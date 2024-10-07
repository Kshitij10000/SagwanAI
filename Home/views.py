from django.shortcuts import render , HttpResponse , redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse 
from .models import (stockdata_live_banner , Contact_us , Ticker , Category,
                     NseStockFinancialData , Profile,Broker, FyersCredentials)
from django.http import JsonResponse
from .yahoo_pull import get_instrument_past_data
import os
import json
from django.conf import settings
from .forms import  ProfileUpdateForm , FyersCredentialsForm 
from .fyers_service import FyersService 
from django.utils import timezone
from datetime import datetime, timedelta 
from urllib.parse import urlparse, parse_qs 

# User Login View
def login_user(request):
    if request.method == 'POST':
        signin_username = request.POST.get('signin_username')
        signin_password = request.POST.get('password')
        user_auth = authenticate(request, username=signin_username, password=signin_password)
        if user_auth is not None:
            login(request, user_auth)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login_user.html')

# User Registration View
def create_user(request):
    if request.method == 'POST':
        signup_username = request.POST.get('signup_username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'create_user.html')

        try:
            user = User.objects.create_user(username=signup_username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login_user')
        except Exception as e:
            messages.error(request, f"Registration failed: {e}")
            return render(request, 'create_user.html')
    else:
        return render(request, 'create_user.html')

# User Logout View
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login_user')

@login_required(login_url='Login')
def home(request):
    return render(request,'dashboard/home.html')

def search_stock():
    pass

# Profile Update View
@login_required(login_url='login_user')
def update_profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'p_form': p_form,
        
    }
    return render(request, 'dashboard/profile.html', context)

@login_required(login_url='login_user')
def profile(request):
    try:
        profile_instance = request.user.profile
    except Profile.DoesNotExist:
        # Optionally, create the profile here if it doesn't exist
        profile_instance = Profile.objects.create(user=request.user)
        messages.info(request, "Profile created for you. You can update it below.")

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        p_form = ProfileUpdateForm(instance=profile_instance)

    
    context = {
        'p_form': p_form,
        
    }
    return render(request, 'dashboard/profile.html', context)

def get_ticker_banner_data(request):
    data = stockdata_live_banner.objects.values('name', 'price')
    return JsonResponse({'stocks': list(data)})


def send_gmail(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_email = request.POST.get('from_email')
        recipients = request.POST.get('recipients').split(',')

        # Sending the email
        try:
            send_mail(subject, message, from_email, recipients)
            messages.success(request, "Email sent successfully!")
        except Exception as e:
            messages.error(request, f"Failed to send email: {str(e)}")
        
        return redirect('email_form') 
    
    return render(request, 'dashboard/email_form.html')

def email_form(request):
    return render(request, 'dashboard/email_form.html')


@login_required(login_url='Login')
def investments(request):
    financial_data = NseStockFinancialData.objects.all().order_by('symbol')
    context = {
        'financial_data': financial_data
    }
    return render(request, 'dashboard/investment.html', context)

# Define the path to watchlist_data folder
WATCHLIST_DATA_PATH = os.path.join(settings.BASE_DIR, 'watchlist_data')

def get_available_categories(request):
    """
    API endpoint to return a list of available categories based on JSON files.
    """
    try:
        files = os.listdir(WATCHLIST_DATA_PATH)
    except FileNotFoundError:
        return JsonResponse({'error': 'Watchlist data folder not found.'}, status=500)
    
    categories = []
    for file in files:
        if file.endswith('.json'):
            # Extract category name by removing ".json"
            category = file.replace('.json', '')
            # Replace underscores with spaces and capitalize appropriately
            category = category.replace('_', ' ').title()
            categories.append(category)
    return JsonResponse({'categories': categories})

def get_stocks_by_category(request):
    """
    API endpoint to return stocks for a selected category.
    Expects 'category' as a GET parameter.
    """
    category = request.GET.get('category', '').strip()
    if not category:
        return JsonResponse({'error': 'No category specified.'}, status=400)
    
    # Normalize category name to match filename
    # Example: "Global Currencies" -> "Global_Currencies.json"
    filename = f"{category.replace(' ', '_')}.json"
    filepath = os.path.join(WATCHLIST_DATA_PATH, filename)
    
    if not os.path.exists(filepath):
        return JsonResponse({'error': f"Category '{category}' not found or no data available."}, status=404)
    
    try:
        with open(filepath, 'r') as f:
            stocks = json.load(f)
        return JsonResponse({'stocks': stocks})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='Login')
def watchlist(request):
    """
    Renders the watchlist page with stocks from the default category.
    """
    default_category = 'India'  # Set your desired default category here
    try:
        category = Category.objects.get(name=default_category)
    except Category.DoesNotExist:
        category = None

    if category:
        tickers = category.tickers.all()
    else:
        tickers = Ticker.objects.none()

    categories = Category.objects.all()

    context = {
        'tickers': tickers,
        'default_category': default_category,
        'categories': categories,  # Pass all categories for dropdowns
    }
    return render(request, 'dashboard/watchlist.html', context)

def get_stocks_by_category(request):
    category_name = request.GET.get('category')
    if not category_name:
        return JsonResponse({'error': 'Category not provided.'}, status=400)

    try:
        category = Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category does not exist.'}, status=404)

    tickers = category.tickers.all().values('symbol', 'name')
    return JsonResponse({'stocks': list(tickers)})

def get_available_categories(request):
    categories = Category.objects.values_list('name', flat=True)
    return JsonResponse({'categories': list(categories)}) 



def get_stock_data_api(request):
    """
    API endpoint to return stock data for a given ticker and period.
    Expects 'ticker' and 'period' as GET parameters.
    """
    ticker = request.GET.get('ticker', '').upper()
    period = request.GET.get('period', '1y')  # Default to 1 year

    if not ticker:
        return JsonResponse({'error': 'No ticker symbol provided.'}, status=400)

    data = get_instrument_past_data(ticker, period)

    if 'error' in data:
        return JsonResponse({'error': data['error']}, status=400)

    return JsonResponse(data)


@login_required
def manage_fyers_credentials(request):
    try:
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
    except FyersCredentials.DoesNotExist:
        fyers_credentials = None

    if request.method == 'POST':
        if fyers_credentials:
            form = FyersCredentialsForm(request.POST, instance=fyers_credentials)
            if form.is_valid():
                form.save()
                messages.success(request, "Fyers credentials updated successfully!")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = FyersCredentialsForm(request.POST)
            if form.is_valid():
                fyers_cred = form.save(commit=False)
                fyers_cred.user = request.user
                fyers_cred.broker = Broker.objects.get(name='Fyers')
                fyers_cred.save()
                messages.success(request, "Fyers credentials added successfully!")
                return redirect('profile')
            else:
                messages.error(request, "Please correct the errors below.")
    else:
        form = FyersCredentialsForm(instance=fyers_credentials)

    context = {
        'form': form,
        'fyers_credentials': fyers_credentials,
    }
    return render(request, 'dashboard/manage_fyers_credentials.html', context)

@login_required
def delete_fyers_credentials(request):
    try:
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
    except FyersCredentials.DoesNotExist:
        fyers_credentials = None

    if not fyers_credentials:
        messages.error(request, "You do not have any Fyers credentials to delete.")
        return redirect('profile')

    if request.method == 'POST':
        fyers_credentials.delete()
        messages.success(request, "Fyers credentials deleted successfully.")
        return redirect('profile')

    return render(request, 'dashboard/delete_fyers_credentials.html', {'fyers_credentials': fyers_credentials})



@login_required
def fyers_manual_redirect_input(request):
    """
    Displays a form to input the redirect URL during development.
    """
    return render(request, 'fyers/manual_redirect_input.html')

# View to handle the manual redirect URL submission
@login_required
def fyers_manual_callback(request):
    """
    Handles the manual redirect URL input during development.
    """
    if request.method == 'POST':
        redirect_url = request.POST.get('redirect_url')
        if not redirect_url:
            messages.error(request, "No redirect URL provided.")
            return redirect('fyers_manual_redirect_input')
        
        # Parse the redirect URL to extract auth_code
        try:
            parsed_url = urlparse(redirect_url)
            query_params = parse_qs(parsed_url.query)
            auth_code = query_params.get('auth_code')
            if not auth_code:
                messages.error(request, "Auth code not found in the redirect URL.")
                return redirect('fyers_manual_redirect_input')
            auth_code = auth_code[0]  # get the first auth_code if multiple
        except Exception as e:
            messages.error(request, f"Failed to parse redirect URL: {str(e)}")
            return redirect('fyers_manual_redirect_input')
        
        # Proceed to generate access token and fetch username
        try:
            fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
        except FyersCredentials.DoesNotExist:
            messages.error(request, "Fyers credentials not found. Please set up your Fyers credentials first.")
            return redirect('manage_fyers_credentials')
        
        fyers_service = FyersService(fyers_credentials)
        try:
            access_token = fyers_service.generate_access_token(auth_code)
        except Exception as e:
            messages.error(request, f"Failed to generate access token: {str(e)}")
            return redirect('fyers_manual_redirect_input')
        
        # Save access token and set token_expiry to current time + 1 day
        fyers_credentials.access_token = access_token
        fyers_credentials.token_expiry = timezone.now() + timedelta(days=1)
        
        # Get username
        try:
            username = fyers_service.get_username(access_token)
        except Exception as e:
            messages.error(request, f"Failed to fetch username: {str(e)}")
            username = None
        
        fyers_credentials.username = username
        fyers_credentials.save()
        
        messages.success(request, "Fyers authentication successful!")
        return render(request, 'fyers/callback_success.html')  # Render success template
    
    else:
        messages.error(request, "Invalid request method.")
        return redirect('fyers_manual_redirect_input')

@login_required
def fyers_authentication(request):
    """
    Renders the Fyers main page and displays the username and funds if available.
    """
    try:
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
    except FyersCredentials.DoesNotExist:
        fyers_credentials = None

    username = None
    funds = None

    if fyers_credentials and fyers_credentials.access_token and fyers_credentials.token_expiry:
        if fyers_credentials.token_expiry > timezone.now():
            # Token is still valid
            fyers_service = FyersService(fyers_credentials)
            try:
                username = fyers_service.get_username(fyers_credentials.access_token)
            except Exception as e:
                messages.error(request, f"Failed to fetch username: {str(e)}")
            
            try:
                funds = fyers_service.get_funds(fyers_credentials.access_token)
            except Exception as e:
                messages.error(request, f"Failed to fetch funds: {str(e)}")
        else:
            # Token expired
            messages.info(request, "Your Fyers access token has expired. Please generate a new auth code.")
    else:
        if fyers_credentials:
            messages.info(request, "Please generate your Fyers auth code.")
        else:
            messages.info(request, "Please set up your Fyers credentials and generate an auth code.")
    
    context = {
        'username': username,
        'funds': funds,
    }
    return render(request, 'fyers/fyers_main.html', context)

# Existing generate_fyers_auth_code view remains unchanged
@login_required
def generate_fyers_auth_code(request):
    """
    Redirects the user to the Fyers authentication URL.
    """
    try:
        # Fetch the user's FyersCredentials
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
    except FyersCredentials.DoesNotExist:
        messages.error(request, "Fyers credentials not found. Please set up your Fyers credentials first.")
        return redirect('manage_fyers_credentials')  # Redirect to credentials management page
    
    # Initialize the FyersService with the user's credentials
    fyers_service = FyersService(fyers_credentials)
    
    # Generate the authentication URL
    auth_url = fyers_service.get_authentication_url()
    
    # Redirect the user to the Fyers authentication URL in a new window
    return redirect(auth_url)

# Existing fyers_callback view remains unchanged for production use
@login_required
def fyers_callback(request):
    """
    Handles the callback from Fyers after user authentication.
    """
    auth_code = request.GET.get('auth_code')
    state = request.GET.get('state')

    if not auth_code:
        messages.error(request, "Authorization code not found.")
        return redirect('fyers_connect')
    
    try:
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
    except FyersCredentials.DoesNotExist:
        messages.error(request, "Fyers credentials not found. Please set up your Fyers credentials first.")
        return redirect('manage_fyers_credentials')

    fyers_service = FyersService(fyers_credentials)
    try:
        access_token = fyers_service.generate_access_token(auth_code)
    except Exception as e:
        messages.error(request, f"Failed to generate access token: {str(e)}")
        return redirect('fyers_connect')

    # Save access token and set token_expiry to current time + 1 day
    fyers_credentials.access_token = access_token
    fyers_credentials.token_expiry = timezone.now() + timedelta(days=1)
    
    # Get username
    try:
        username = fyers_service.get_username(access_token)
    except Exception as e:
        messages.error(request, f"Failed to fetch username: {str(e)}")
        username = None
    
    fyers_credentials.username = username
    fyers_credentials.save()

    messages.success(request, "Fyers authentication successful!")
    return render(request, 'fyers/callback_success.html')

@login_required
def fyers_logout(request):
    """
    Logs out the user from Fyers by clearing their access tokens and related data.
    """
    try:
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
        # Clear sensitive fields
        fyers_credentials.access_token = None
        fyers_credentials.token_expiry = None
        fyers_credentials.username = None
        fyers_credentials.save()
        messages.success(request, "Successfully logged out from Fyers.")
    except FyersCredentials.DoesNotExist:
        messages.info(request, "No Fyers session found to log out.")
    
    return redirect('fyers_connect')










def finnifty(request):
    return render(request,'dashboard/finnifty.html')

def midcapnifty(request):
    return HttpResponse("This is contact page") 

def send_report(request):
    return render(request,'dashboard/send_report.html')

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        date_time = datetime.now()
        contact_data = Contact_us(name=name,email=email,phone=phone,desc=desc,date_time=date_time)
        contact_data.save()
        messages.success(request, "Your message is sent.")
    return render(request,'dashboard/contactus.html') 


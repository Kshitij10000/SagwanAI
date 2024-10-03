from django.shortcuts import render , HttpResponse , redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse 
from .models import stockdata_live_banner , Contact_us , NseTickers , NseStockFinancialData
from django.http import JsonResponse
from .yahoo_pull import get_instrument_past_data
import os
import json
from django.conf import settings


def login_user(request):
    if request.method == 'POST':
        signin_username = request.POST.get('signin_username')
        signin_password = request.POST.get('password')
        user_auth = authenticate(request,username = signin_username , password = signin_password)
        if user_auth is not None:
            login(request,user_auth)
            return redirect('/home')
        else: 
            print("login id is wrong")
    return render(request,'login.html') 

def registration_user(request):
    if request.method == 'POST':
        signup_name = request.POST.get('signup_username')
        signup_email = request.POST.get('email')
        signup_password = request.POST.get('password')
        signup_confirm_password = request.POST.get('confirm_password')

        if signup_password != signup_confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'registration.html')

        try:
            if User.objects.filter(username=signup_name).exists():
                messages.error(request, "Username already taken. Please choose a different username.")
                return render(request, 'registration.html')

            user = User.objects.create_user(username=signup_name, email=signup_email, password=signup_password)
            messages.success(request, "Registration successful!")

            return redirect('Login')  # Redirect to a success page or login page
        except IntegrityError:
            messages.error(request, "A user with that username already exists.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'registration.html')

def logout_user(request):
    logout(request)
    return redirect('Login')

@login_required(login_url='Login')
def home(request):
    return render(request,'home.html')

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
    
    return render(request, 'email_form.html')

def email_form(request):
    return render(request, 'email_form.html')


@login_required(login_url='Login')
def investments(request):
    financial_data = NseStockFinancialData.objects.all().order_by('symbol')
    context = {
        'financial_data': financial_data
    }
    return render(request, 'investment.html', context)

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
    filename = f"{default_category.replace(' ', '_')}.json"
    filepath = os.path.join(WATCHLIST_DATA_PATH, filename)
    
    if not os.path.exists(filepath):
        stocks = []
    else:
        with open(filepath, 'r') as f:
            stocks = json.load(f)
    
    context = {
        'tickers': stocks,
        'default_category': default_category
    }
    return render(request, 'watchlist.html', context)

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

































def banknifty(request):
    return render(request,'banknifty.html')

def finnifty(request):
    return render(request,'finnifty.html')

def midcapnifty(request):
    return HttpResponse("This is contact page") 

def send_report(request):
    return render(request,'send_report.html')

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
    return render(request,'contactus.html') 


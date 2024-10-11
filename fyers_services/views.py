from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Home.models import Broker
from .models import FyersCredentials 
from django.http import JsonResponse
from django.conf import settings
from .forms import FyersCredentialsForm 
from .fyers_service import FyersService 
from django.utils import timezone
from datetime import  timedelta 
from urllib.parse import urlparse, parse_qs 

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
def get_trade_book_api(request):
    """
    API endpoint to return the trade book data.
    """
    try:
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
        if fyers_credentials.access_token and fyers_credentials.token_expiry > timezone.now():
            fyers_service = FyersService(fyers_credentials)
            trade_book = fyers_service.get_trade_book(fyers_credentials.access_token)
            if trade_book is not None:
                return JsonResponse({'trade_book': trade_book})
            else:
                return JsonResponse({'error': 'Failed to retrieve trade book data.'}, status=500)
        else:
            return JsonResponse({'error': 'Invalid or expired access token.'}, status=401)
    except FyersCredentials.DoesNotExist:
        return JsonResponse({'error': 'Fyers credentials not found.'}, status=404)

@login_required
def fyers_main_with_trade_book(request):
    """
    Renders the Fyers main page with the trade book visible by default.
    """
    try:
        fyers_credentials = FyersCredentials.objects.get(user=request.user, broker__name='Fyers')
    except FyersCredentials.DoesNotExist:
        fyers_credentials = None

    username = None
    funds = None
    trade_book = []
    positions = []

    if fyers_credentials and fyers_credentials.access_token and fyers_credentials.token_expiry:
        if fyers_credentials.token_expiry > timezone.now():
            fyers_service = FyersService(fyers_credentials)
            try:
                username = fyers_service.get_username(fyers_credentials.access_token)
            except Exception as e:
                messages.error(request, f"Failed to fetch username: {str(e)}")
            
            try:
                funds = fyers_service.get_funds(fyers_credentials.access_token)
            except Exception as e:
                messages.error(request, f"Failed to fetch funds: {str(e)}")
            
            try:
                trade_book = fyers_service.get_trade_book(fyers_credentials.access_token)
                if not trade_book:
                    messages.info(request, "No trade book data available.")
            except Exception as e:
                messages.error(request, f"Failed to fetch trade book: {str(e)}")
            
            try:
                positions = fyers_service.get_positions(fyers_credentials.access_token)  # Ensure this method exists
                if not positions:
                    messages.info(request, "No positions data available.")
            except Exception as e:
                messages.error(request, f"Failed to fetch positions: {str(e)}")
        else:
            messages.info(request, "Your Fyers access token has expired. Please generate a new auth code.")
    else:
        if fyers_credentials:
            messages.info(request, "Please generate your Fyers auth code.")
        else:
            messages.info(request, "Please set up your Fyers credentials and generate an auth code.")
    
    context = {
        'username': username,
        'funds': funds,
        'trade_book': trade_book,
        'positions': positions,
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

from django.urls import path 
from . import views  # Import views from fyers_services app

urlpatterns = [
    path('', views.fyers_main_with_trade_book, name='fyers_connect'), 

    # Fyers Credentials URLs
    path('profile/fyers_credentials/', views.manage_fyers_credentials, name='manage_fyers_credentials'),
    path('profile/fyers_credentials/delete/', views.delete_fyers_credentials, name='delete_fyers_credentials'),

    # URL for generating Fyers Auth Code
    path('fyers/generate_auth_code/', views.generate_fyers_auth_code, name='generate_fyers_auth_code'),

    # Callback URL for Fyers Authentication
    path('fyers/callback/', views.fyers_callback, name='fyers_callback'),

    # Manual Redirect URL Input
    path('fyers/manual_redirect_input/', views.fyers_manual_redirect_input, name='fyers_manual_redirect_input'),
    path('fyers/manual_callback/', views.fyers_manual_callback, name='fyers_manual_callback'),

    # Fyers Logout URL
    path('fyers/logout/', views.fyers_logout, name='fyers_logout'),  
    
    # New Trade Book API URL
    path('api/get_trade_book/', views.get_trade_book_api, name='get_trade_book_api'),
]
from django.contrib import admin
from django.urls import path 
from Home import views 
from django.shortcuts import redirect
from . import views


urlpatterns = [
    path('', lambda request: redirect('login_user'), name='root'),
    path('login/', views.login_user , name='login_user'),
    path('create_user/', views.create_user , name='create_user'),
    path('logout/', views.logout_user , name='logout'),
    path('investment_options/', views.investments, name='investment_options'),
    path('home/', views.home , name='home'),
    path('search_stock/', views.search_stock, name='search_stock'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('banknifty/', views.banknifty, name='banknifty'),
    path('finnifty/', views.finnifty, name='finnifty'),
    path('midcapnifty/', views.midcapnifty, name='midcapnifty'),
    path('contactus/', views.contactus , name='contactus'),
    path('send_gmail/', views.send_gmail, name='send_gmail'),
    path('email_form/', views.email_form, name='email_form'),
    path('api/v1/market-data-live/home-banner-tickers', views.get_ticker_banner_data, name='API_Banner_ticker_live'), # api for stock ticker banner
    path('api/get_stock_data/', views.get_stock_data_api, name='get_stock_data_api'),
    path('api/get_available_categories/', views.get_available_categories, name='get_available_categories'),
    path('api/get_stocks_by_category/', views.get_stocks_by_category, name='get_stocks_by_category'),

    # Fyers Credentials URLs
    path('profile/fyers_credentials/', views.manage_fyers_credentials, name='manage_fyers_credentials'),
    path('profile/fyers_credentials/delete/', views.delete_fyers_credentials, name='delete_fyers_credentials'),
    
]

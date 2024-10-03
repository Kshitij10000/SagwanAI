from django.contrib import admin
from django.urls import path 
from Home import views 
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('Login'), name='root'),
    path('login', views.login_user , name='Login'),
    path('registration/', views.registration_user , name='registration'),
    path('logout', views.logout_user , name='logout'),
    path('investment_options', views.investments, name='investments'),
    path('home', views.home , name='Home'),
    path('watchlist', views.watchlist , name='watchlist'),
    path('banknifty', views.banknifty , name='Services'),
    path('finnifty', views.finnifty , name='Contact'),
    path('midcapnifty', views.midcapnifty , name='Contact'),
    path('contactus', views.contactus , name='Contact'),
    path('send_gmail', views.send_gmail, name='send_gmail'),
    path('email_form', views.email_form, name='email_form'),
    path('api/v1/market-data-live/home-banner-tickers', views.get_ticker_banner_data, name='API_Banner_ticker_live'), # api for stock ticker banner
    path('api/get_stock_data/', views.get_stock_data_api, name='get_stock_data_api'),
    path('api/get_available_categories/', views.get_available_categories, name='get_available_categories'),
    path('api/get_stocks_by_category/', views.get_stocks_by_category, name='get_stocks_by_category'),
    
]

# paper_trade/urls.py

from django.urls import path
from . import views

app_name = 'paper_trade'

urlpatterns = [
    path('broker_main/', views.broker_main, name='broker_main'),
    path('place_order/', views.place_order, name='place_order'),
    path('trade_book/', views.trade_book, name='trade_book'),
    path('positions/', views.positions, name='positions'),
    path('exit_position/', views.exit_position, name='exit_position'),
]

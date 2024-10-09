from django.urls import path
from . import views 

urlpatterns = [
    path('', views.synth_paper_broker, name='synth_paper_broker'),
    path('api/get_live_stock_prices/', views.get_live_stock_prices, name='get_live_stock_prices'),
    path('api/get_order_book/', views.get_order_book, name='get_order_book'),
    path('api/get_position_book/', views.get_position_book, name='get_position_book'),
    # Add more PaperTrade-specific URLs here if needed
]
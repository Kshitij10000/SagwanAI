# paper_trade/admin.py

from django.contrib import admin
from .models import Order, Position

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticker', 'order_type', 'execution_type', 'price', 'quantity', 'funds_needed', 'status', 'created_at')
    list_filter = ('order_type', 'execution_type', 'status', 'created_at')
    search_fields = ('user__username', 'ticker')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ticker', 'quantity', 'average_price', 'current_price', 'pnl')
    list_filter = ('ticker', 'user')
    search_fields = ('user__username', 'ticker')

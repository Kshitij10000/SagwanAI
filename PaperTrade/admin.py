from django.contrib import admin
from .models import Fund, Order, Position, Trade

@admin.register(Fund)
class FundAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')  # Only existing fields
    search_fields = ('user__username',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticker', 'order_type', 'quantity', 'price', 'status', 'created_at')
    list_filter = ('order_type', 'status')
    search_fields = ('user__username', 'ticker__symbol')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ticker', 'quantity', 'average_price', 'current_price', 'pnl')
    search_fields = ('user__username', 'ticker__symbol')

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('order', 'executed_quantity', 'executed_price', 'executed_at')
    search_fields = ('order__user__username', 'order__ticker__symbol')

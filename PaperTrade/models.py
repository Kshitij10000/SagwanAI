from django.db import models
from django.contrib.auth.models import User
from Home.models import Ticker  

class Fund(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='funds')
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=100000.00)

    def __str__(self):
        return f"{self.user.username}'s Fund"



class Order(models.Model):
    ORDER_TYPES = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('EXECUTED', 'Executed'),
        ('CANCELLED', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_type} {self.quantity} {self.ticker.symbol} by {self.user.username}"


class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='positions')
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pnl = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Profit & Loss

    def __str__(self):
        return f"{self.ticker.symbol} - {self.user.username}"

class Trade(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='trades')
    executed_quantity = models.PositiveIntegerField()
    executed_price = models.DecimalField(max_digits=10, decimal_places=2)
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trade for {self.order.ticker.symbol} by {self.order.user.username}"


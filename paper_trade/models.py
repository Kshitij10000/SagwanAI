# paper_trade/models.py

from django.db import models
from django.contrib.auth.models import User

ORDER_TYPE_CHOICES = [
    ('BUY', 'Buy'),
    ('SELL', 'Sell'),
]

EXECUTION_TYPE_CHOICES = [
    ('MARKET', 'Market'),
    ('LIMIT', 'Limit'),
]

ORDER_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('EXECUTED', 'Executed'),
    ('CANCELLED', 'Cancelled'),
]

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(
        max_length=100,
        default='UNKNOWN',  # Default value added
        help_text="Ticker symbol of the financial instrument"
    )
    order_type = models.CharField(max_length=4, choices=ORDER_TYPE_CHOICES)
    execution_type = models.CharField(
        max_length=7,
        choices=EXECUTION_TYPE_CHOICES,
        default='MARKET'  # Ensure this has a default as well
    )
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField()
    funds_needed = models.DecimalField(max_digits=20, decimal_places=2)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_type} {self.quantity} {self.ticker} at {self.price}"

class Position(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    average_price = models.DecimalField(max_digits=20, decimal_places=2)
    current_price = models.DecimalField(max_digits=20, decimal_places=2)
    pnl = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.ticker} Position for {self.user.username}"

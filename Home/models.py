from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class Contact_us(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    desc = models.TextField()
    date_time = models.DateField() 
    
    def __str__(self):
        return self.name



class stockdata_live_banner(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}: {self.price}"


class NseTickers(models.Model):
    symbol = models.CharField(max_length=50, unique=True,db_index=True)
    name_of_company = models.CharField(max_length=100)	
    series = models.CharField(max_length=10)	
    date_of_listing = models.DateField()
    paid_up_value = models.DecimalField(max_digits=10, decimal_places=2)
    market_lot = models.IntegerField()
    ISIN_number = models.CharField(max_length=50, unique=True)
    face_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name = "NSE Ticker"
        verbose_name_plural = "NSE Tickers"


class NseStockFinancialData(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    long_name = models.CharField(max_length=255, null=True, blank=True)
    ebitda = models.BigIntegerField(null=True, blank=True)
    previous_close = models.FloatField(null=True, blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    total_revenue = models.BigIntegerField(null=True, blank=True)
    net_income_to_common = models.BigIntegerField(null=True, blank=True)
    total_cash = models.BigIntegerField(null=True, blank=True)
    revenue_per_share = models.FloatField(null=True, blank=True)
    total_cash_per_share = models.FloatField(null=True, blank=True)
    two_hundred_day_average = models.FloatField(null=True, blank=True)
    fifty_day_average = models.FloatField(null=True, blank=True)
    float_shares = models.BigIntegerField(null=True, blank=True)
    held_percent_insiders = models.FloatField(null=True, blank=True)
    held_percent_institutions = models.FloatField(null=True, blank=True)
    implied_shares_outstanding = models.BigIntegerField(null=True, blank=True)
    
    
    def __str__(self):
        return self.symbol 
    

# Profile model extending User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields as needed
    # Example:
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
  
class Broker(models.Model):
    name = models.CharField(max_length=50, unique=True)
    api_documentation_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


    
# watchlist models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name 

class All_Ticker(models.Model):
    symbol = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='tickers', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.symbol} - {self.name}"        
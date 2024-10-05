from django.contrib import admin
from Home.models import (Contact_us ,stockdata_live_banner , Live_Stock_Banner_Ticker , NseTickers , 
                         NseStockFinancialData ,Profile ,Broker , FyersCredentials , Category , Ticker)
from .resources import NseTickersResource 
from import_export.admin import ImportExportModelAdmin


# Register your models here.

@admin.register(Contact_us)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ( 'name','email','phone', 'desc', 'date_time')
    search_fields = ('email' , 'phone')


@admin.register(stockdata_live_banner)
class StockDataLiveBannerAdmin(admin.ModelAdmin):
   list_display = ('name' , 'price' , 'last_updated')
   

@admin.register(Live_Stock_Banner_Ticker)
class LiveStockDataBannerAdmin(admin.ModelAdmin):
    list_display = ('name' , 'ticker')

@admin.register(NseTickers)
class NseTickersAdmin(ImportExportModelAdmin):
    resource_class = NseTickersResource
    list_display = (
        'symbol',
        'name_of_company',
        'series',
        'date_of_listing',
        'paid_up_value',
        'market_lot',
        'ISIN_number',
        'face_value',
    )
    search_fields = ('symbol', 'name_of_company', 'ISIN_number') 

@admin.register(NseStockFinancialData)
class StockFinancialDataAdmin(admin.ModelAdmin):
    list_display = (
        'symbol', 'previous_close', 'market_cap', 'total_revenue', 
        'net_income_to_common', 'total_cash', 'revenue_per_share', 
        'total_cash_per_share', 'two_hundred_day_average', 'fifty_day_average', 
        'float_shares', 'held_percent_insiders', 'held_percent_institutions', 
        'implied_shares_outstanding', 'long_name', 'ebitda'
    )
    search_fields = ('symbol',) 
  
@admin.register(Profile)  
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_image')
    search_fields = ('user__username', 'user__email')


@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_documentation_url')
    search_fields = ('name',)

@admin.register(FyersCredentials)
class FyersCredentialsAdmin(admin.ModelAdmin):
    list_display = ('user', 'broker', 'ttop_key', 'client_id', 'created_at', 'updated_at')
    search_fields = ('user__username', 'ttop_key', 'client_id')
    list_filter = ('broker', 'created_at')
    readonly_fields = ('created_at', 'updated_at')  # Prevent editing timestamps


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Ticker)
class TickerAdmin(admin.ModelAdmin):
    list_display = ['id', 'symbol', 'name', 'category']
    search_fields = ['symbol', 'name']
    list_filter = ['category']
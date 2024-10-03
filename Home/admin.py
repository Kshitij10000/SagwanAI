from django.contrib import admin
from Home.models import Contact_us ,stockdata_live_banner , Live_Stock_Banner_Ticker , NseTickers , NseStockFinancialData
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
  
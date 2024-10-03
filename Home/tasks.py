from celery.utils.log import get_task_logger
from celery import shared_task
from .yahoo_pull import fetch_Live_data
from .models import stockdata_live_banner, NseStockFinancialData, NseTickers
from django.db import transaction
import yfinance as yf
import pandas as pd
import logging
import math
 
logger = get_task_logger(__name__)

@shared_task(bind=True)
def fetch_live_tocker_data(self):
    logger.info("Starting fetch_live_tocker_data task.")
    try:
        data = fetch_Live_data()
        for name, price in data.items():
            if price not in ["No data available", "Timeout"] and not price.startswith("Error:"):
                stockdata_live_banner.objects.update_or_create(name=name, defaults={'price': price})
                logger.info(f"Updated {name} with price {price}.")
            else:
                logger.warning(f"Data not available or error for {name}: {price}. Skipping.")
        logger.info("Completed fetch_live_tocker_data task.")
    except Exception as e:
        logger.error(f"An error occurred while fetching stock data: {str(e)}", exc_info=True)


def safe_value(value):
    """Convert NaN to None for database fields."""
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

@shared_task
def process_stock_data():
    logger.info("Task started: Fetching stock data.")
    try:
        Symbols = NseTickers.objects.values_list('symbol', flat=True)
        logger.debug(f"Symbols to process: {list(Symbols)}")
        
        all_stock_list = []
        for symbol in Symbols:
            logger.debug(f"Processing symbol: {symbol}")
            try:
                stock = yf.Ticker(f"{symbol}.NS")
                info = stock.info
                logger.debug(f"Fetched info for {symbol}: {info}")
                
                data = {
                    'Symbol': info.get('symbol'),
                    'Long_Name': info.get('longName'),
                    'Previous_Close': safe_value(info.get('previousClose')),
                    'Market_Cap': safe_value(info.get('marketCap')),
                    'Total_Revenue': safe_value(info.get('totalRevenue')),
                    'NetIncome': safe_value(info.get('netIncomeToCommon')),
                    'Total_Cash': safe_value(info.get('totalCash')),
                    'Ebitda': safe_value(info.get('ebitda')),
                    'Revenue_Per_Share': safe_value(info.get('revenuePerShare')),
                    'Total_Cash_Per_Share': safe_value(info.get('totalCashPerShare')),
                    'Two_Hundred_Day_Average': safe_value(info.get('twoHundredDayAverage')),
                    'Fifty_Day_Average': safe_value(info.get('fiftyDayAverage')),
                    'Float_Shares': safe_value(info.get('floatShares')),
                    'Held_Percent_Insiders': safe_value(info.get('heldPercentInsiders')),
                    'Held_Percent_Institutions': safe_value(info.get('heldPercentInstitutions')),
                    'Implied_Shares_Outstanding': safe_value(info.get('impliedSharesOutstanding')),
                    
                    # New fields
                    'target_median_price': safe_value(info.get('targetMedianPrice')),
                    'open_price': safe_value(info.get('open')),
                    'high_price': safe_value(info.get('high')),
                    'low_price': safe_value(info.get('low')),
                    'volume': safe_value(info.get('volume')),
                }

                all_stock_list.append(data)
                logger.debug(f"Appended data for {symbol}")
            except Exception as e:
                logger.error(f"Error fetching data for {symbol}: {e}")
        
        # Create DataFrame
        all_stock_dataframe = pd.DataFrame(all_stock_list)
        logger.debug(f"Created DataFrame with {len(all_stock_dataframe)} records.")
        
        # Update or create records
        for index, row in all_stock_dataframe.iterrows():
            symbol = row['Symbol']
            logger.debug(f"Updating data for symbol: {symbol}")
            try:
                # Map DataFrame columns to model fields
                defaults = {
                    'long_name': row['Long_Name'],
                    'previous_close': row['Previous_Close'],
                    'market_cap': row['Market_Cap'],
                    'total_revenue': row['Total_Revenue'],
                    'net_income_to_common': row['NetIncome'],
                    'total_cash': row['Total_Cash'],
                    'ebitda': row['Ebitda'],
                    'revenue_per_share': row['Revenue_Per_Share'],
                    'total_cash_per_share': row['Total_Cash_Per_Share'],
                    'two_hundred_day_average': row['Two_Hundred_Day_Average'],
                    'fifty_day_average': row['Fifty_Day_Average'],
                    'float_shares': row['Float_Shares'],
                    'held_percent_insiders': row['Held_Percent_Insiders'],
                    'held_percent_institutions': row['Held_Percent_Institutions'],
                    'implied_shares_outstanding': row['Implied_Shares_Outstanding'],
                    
                    # New fields
                    'target_median_price': row['target_median_price'],
                    'open_price': row['open_price'],
                    'high_price': row['high_price'],
                    'low_price': row['low_price'],
                    'volume': row['volume'],
                }

                # Update or create the record
                NseStockFinancialData.objects.update_or_create(
                    symbol=symbol,
                    defaults=defaults
                )
                logger.debug(f"Updated NseStockFinancialData for {symbol}")
            except Exception as e:
                logger.error(f"Error updating data for {symbol}: {e}")
        
        logger.info("Task completed: Stock data processed successfully.")
        return "Stock data processed successfully."
    except Exception as e:
        logger.error(f"An error occurred in process_stock_data: {e}", exc_info=True)
        raise e
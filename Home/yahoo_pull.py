import yfinance as yf
from .models import  All_Ticker
import logging

logger = logging.getLogger(__name__)

def fetch_Live_data():
    timeout_setting = 10  
    data = {}
    stocks = All_Ticker.objects.only('name','symbol')  

    for stock in stocks:
        ticker = yf.Ticker(stock.symbol)
        try:
            current_data = ticker.history(period="1d", timeout=timeout_setting)
            if not current_data.empty:
                close_price = current_data['Close'].iloc[-1]
                data[stock.name] = format(close_price, ".2f")
            else:
                data[stock.name] = "No data available"
        except IndexError as ie:
            data[stock.name] = "No data available"
            logger.error(f"No data available for {stock.name}: {ie}")
        except Exception as e:
            data[stock.name] = f"Error: {str(e)}"
            logger.error(f"Error fetching data for {stock.name}: {e}")

    return data


def get_instrument_past_data(ticker, period='1y'):
   
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)

        if hist.empty:
            return {'error': f"No historical data found for ticker '{ticker}'."}

        info = stock.info
        company_name = info.get('longName', 'N/A')
        exchange = info.get('exchange', 'N/A')

        # Prepare historical data
        historical_data = hist.reset_index().to_dict(orient='records')

        # Format dates
        for entry in historical_data:
            entry['Date'] = entry['Date'].strftime('%Y-%m-%d')

        return {
            'company_name': company_name,
            'exchange': exchange,
            'historical_data': historical_data
        }

    except Exception as e:
        return {'error': str(e)}

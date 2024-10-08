# Home/fyers_service.py
from urllib.parse import urlencode
from fyers_apiv3 import fyersModel 
from django.utils import timezone
from asgiref.sync import async_to_sync
import logging 

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class FyersService:
    def __init__(self, credentials):
        self.client_id = credentials.client_id
        self.secret_key = credentials.secret_key
        self.redirect_uri = credentials.redirect_uri
        self.state = credentials.state
        self.base_auth_url = "https://api.fyers.in/api/v2/generate-authcode"

    def get_authentication_url(self):
        """
        Generates the Fyers authentication URL using the user's credentials.
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'state': self.state,
        }
        query_string = urlencode(params)
        return f"{self.base_auth_url}?{query_string}"
    
    def generate_access_token(self, auth_code):
        """
        Generates the access token using the authorization code.
        """
        grant_type = "authorization_code"  

        # Create a session object to handle the Fyers API authentication and token generation
        session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key, 
            redirect_uri=self.redirect_uri, 
            response_type='code', 
            grant_type=grant_type
        )

        # Set the authorization code in the session object
        session.set_token(auth_code)

        # Generate the access token using the authorization code
        response = session.generate_token()
        
        if 'access_token' in response:
            access_token = response['access_token'] 
            return access_token
        else:
            raise Exception("Failed to generate access token.")
    
    def get_username(self, access_token):
        """
        Retrieves the username from Fyers using the access token.
        """
        # Initialize the FyersModel instance with your client_id and access_token
        fyers = fyersModel.FyersModel(client_id=self.client_id, is_async=False, token=access_token, log_path="")
    
        # Make a request to get the user profile information
        response = fyers.get_profile()
        if 'data' in response and 'name' in response['data']:
            return response['data']['name']
        return 'Unknown'
    
    async def get_funds_async(self, access_token):
        """
        Asynchronously retrieves the funds information from Fyers using the access token.
        """
        try:
            # Initialize the FyersModel instance with async mode enabled
            fyers = fyersModel.FyersModel(client_id=self.client_id, token=access_token, is_async=True, log_path="")
    
            # Make an asynchronous request to get the funds information
            response = await fyers.funds()
    
            # Check if the response indicates success
            if response.get("s") == "ok":
                fund_limit = response.get("fund_limit", [])
                funds = {}
    
                # Iterate over each fund detail in 'fund_limit'
                for item in fund_limit:
                    title = item.get('title')
                    equity = item.get('equityAmount', 0)
                    commodity = item.get('commodityAmount', 0)
                    funds[title] = {'equityAmount': equity, 'commodityAmount': commodity}
    
                # Extract desired fields based on their titles
                total_balance = funds.get("Total Balance", {}).get("equityAmount", "N/A")
                available_balance = funds.get("Available Balance", {}).get("equityAmount", "N/A")
                utilized_amount = funds.get("Utilized Amount", {}).get("equityAmount", "N/A")
                clear_balance = funds.get("Clear Balance", {}).get("equityAmount", "N/A")
                # Add more fields as needed
    
                # Return the structured funds data
                return {
                    'total_balance': total_balance,
                    'available_balance': available_balance,
                    'utilized_amount': utilized_amount,
                    'clear_balance': clear_balance,
                }
            else:
                # If response status is not "ok", return None
                return None
    
        except Exception as e:
            # Log the exception if needed
            return None
    
    def get_funds(self, access_token):
        """
        Synchronously retrieves the funds information by running the async function.
        """
        return async_to_sync(self.get_funds_async)(access_token)
    
    def get_trade_book(self, access_token):
        """
        Retrieves the trade book information from Fyers using the access token.
        """
        try:
            # Initialize the FyersModel instance with async mode disabled (synchronous)
            fyers = fyersModel.FyersModel(client_id=self.client_id, token=access_token, is_async=False, log_path="")
    
            # Make a synchronous request to get the trade book information
            response = fyers.tradebook()
    
            # Check if the response indicates success
            if response.get("s") == "ok":
                trade_book = response.get("tradeBook", [])
                trades = []
    
                # Iterate over each trade detail in 'tradeBook'
                for trade in trade_book:
                    # Extract desired fields with snake_case keys
                    trade_info = {
                        'client_id': trade.get('clientId', 'N/A'),
                        'exchange': trade.get('exchange', 'N/A'),
                        'fy_token': trade.get('fyToken', 'N/A'),
                        'order_number': trade.get('orderNumber', 'N/A'),
                        'exchange_order_no': trade.get('exchangeOrderNo', 'N/A'),
                        'trade_number': trade.get('tradeNumber', 'N/A'),
                        'trade_price': trade.get('tradePrice', 'N/A'),
                        'segment': trade.get('segment', 'N/A'),
                        'product_type': trade.get('productType', 'N/A'),
                        'traded_quantity': trade.get('tradedQty', 'N/A'),
                        'symbol': trade.get('symbol', 'N/A'),
                        'row': trade.get('row', 'N/A'),
                        'order_datetime': trade.get('orderDateTime', 'N/A'),
                        'trade_value': trade.get('tradeValue', 'N/A'),
                        'side': 'Buy' if trade.get('side') == 1 else 'Sell',
                        'order_type': trade.get('orderType', 'N/A'),
                        'order_tag': trade.get('orderTag', 'N/A')
                    }
                    trades.append(trade_info)
    
                return trades  # Return the list of trades as dictionaries
    
            else:
                return None  # Indicate failure to retrieve trade book
    
        except Exception as e:
            return None  # Indicate an error occurred 
        
    def get_positions(self, access_token):
        """
        Retrieves the positions information from Fyers using the access token.
        """
        try:
            fyers = fyersModel.FyersModel(client_id=self.client_id, token=access_token, is_async=False, log_path="")

            # Make a synchronous request to get the positions information
            response = fyers.positions()

            # Log the raw API response for debugging
            logger.debug(f"Positions API Response: {response}")

            if response.get("s") == "ok":
                positions = response.get("netPositions", [])  # Changed from 'positions' to 'netPositions' as per working script
                position_list = []

                for position in positions:
                    # Interpret the 'side' field
                    side_value = position.get('side')
                    if side_value == 1:
                        side = 'Long'
                    elif side_value == -1:
                        side = 'Short'
                    else:
                        side = 'Neutral'  # Assuming 0 represents Neutral

                    position_info = {
                        'symbol': position.get('symbol', 'N/A'),
                        'buy_quantity': position.get('buyQty', 'N/A'),
                        'buy_average_price': position.get('buyAvg', 'N/A'),
                        'buy_value': position.get('buyVal', 'N/A'),
                        'sell_quantity': position.get('sellQty', 'N/A'),
                        'sell_average_price': position.get('sellAvg', 'N/A'),
                        'sell_value': position.get('sellVal', 'N/A'),
                        'net_average_price': position.get('netAvg', 'N/A'),
                        'net_quantity': position.get('netQty', 'N/A'),
                        'side': side,
                        'product_type': position.get('productType', 'N/A'),
                        'realized_profit': position.get('realized_profit', 'N/A'),
                        'unrealized_profit': position.get('unrealized_profit', 'N/A'),
                        'profit_loss': position.get('pl', 'N/A'),
                        'last_traded_price': position.get('ltp', 'N/A'),
                        'exchange': position.get('exchange', 'N/A'),
                        'segment': position.get('segment', 'N/A'),
                        'day_buy_qty': position.get('dayBuyQty', 'N/A'),
                        'day_sell_qty': position.get('daySellQty', 'N/A'),
                        'cf_buy_qty': position.get('cfBuyQty', 'N/A'),
                        'cf_sell_qty': position.get('cfSellQty', 'N/A'),
                        'qty_multiplier': position.get('qtyMulti_com', 'N/A'),
                        'fyToken': position.get('fyToken', 'N/A'),
                        'rbi_ref_rate': position.get('rbiRefRate', 'N/A'),
                        'cross_currency': position.get('crossCurrency', 'N/A'),
                        'slNo': position.get('slNo', 'N/A')
                    }

                    position_list.append(position_info)

                logger.debug(f"Processed Positions: {position_list}")
                return position_list

            else:
                logger.error(f"Failed to retrieve positions data. Response: {response}")
                return None

        except Exception as e:
            logger.exception("An error occurred while fetching positions.")
            return None
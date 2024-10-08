import asyncio
from fyers_apiv3 import fyersModel  # Ensure this is the correct import based on the Fyers API documentation
import sys 
import os 
import pandas as pd
# Replace these with your actual credentials
CLIENT_ID = "Y25P4GTMHA-100"
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3Mjg0MTczODMsImV4cCI6MTcyODQzMzgyMywibmJmIjoxNzI4NDE3MzgzLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbkJZNW5BQlhXWUJNX1ZVQXVOZDlPM2xabV9JVDR2Q1RTUF9MelFCam9lVVJaUUpfT09oYkxyT3ZGb2w2X0RfVDFvZjZ3Rnl6TVlOYUhkUkxoUGR4UW5FTzFWQVQ5ejloWEtFS0xsVzRRQjIzTEg0az0iLCJkaXNwbGF5X25hbWUiOiJLU0hJVElKIERJTElQIFNBUlZFIiwib21zIjoiSzEiLCJoc21fa2V5IjoiZjk3YmNjODgyZWM5MWUxNDA5NTU3NWE2NGM5MmQ0M2Y4MDkzYmU0MDE5NmIzMGI2YTlmNDU2MWIiLCJmeV9pZCI6IlhLMDMwNjEiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.Fn8VtRBHlDcu8tk0Oi06F0NM4GGYIKM9DaQxIT3KQHw'


def get_positionbook_sync(client_id: str, access_token: str):
    """
    Synchronously retrieves trade book information from the Fyers API.

    Args:
        client_id (str): Your Fyers API client ID.
        access_token (str): Your Fyers API access token.

    Returns:
        pd.DataFrame: DataFrame containing trade book information.
    """
    try:
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")
    
        # Make a synchronous request to get the positions information
        response = fyers.positions()

    

        if response.get("s") == "ok":
            positions = response.get("netPositions", [])
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
                
                # Append inside the loop
                position_list.append(position_info)

            # Convert the list of trades to a DataFrame for better presentation
            df_trades = pd.DataFrame(position_list)

            print("\nTrade Book Information:")
            print(df_trades)

        

        else:
            print("\nFailed to retrieve trade book data.")
            print("Response:", response)
            return pd.DataFrame()

    except Exception as e:
        print(f"\nAn error occurred while fetching trade book data: {e}")
        return pd.DataFrame()

def main():
    """
    Entry point for the script.
    """
    # Validate credentials
    if CLIENT_ID == "YOUR_CLIENT_ID" or ACCESS_TOKEN == "YOUR_ACCESS_TOKEN":
        print("Please replace 'YOUR_CLIENT_ID' and 'YOUR_ACCESS_TOKEN' with your actual Fyers API credentials.")
        sys.exit(1)

    # Fetch and process trade book data
    get_positionbook_sync(CLIENT_ID, ACCESS_TOKEN)

if __name__ == "__main__":
    main()
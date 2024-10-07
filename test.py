import asyncio
from fyers_apiv3 import fyersModel  # Ensure this is the correct import based on the Fyers API documentation
import sys 
import os 
import pandas as pd
# Replace these with your actual credentials
CLIENT_ID = "Y25P4GTMHA-100"
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MjgzMDM1NzUsImV4cCI6MTcyODM0NzQzNSwibmJmIjoxNzI4MzAzNTc1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbkE5SFhXOGx0d3JYdVRfTFAteTJRTkxWSWpkV1UyTUpoZEp5WW5lV1hJZEI5N1hKb29mSFRON002Q0d4TFBqOEgzNGpDLUVVU1FLNThfc2JYeVRpTm1vOTRuX0t6VnJPRndwUzA0M1MzbUlGM1RoND0iLCJkaXNwbGF5X25hbWUiOiJLU0hJVElKIERJTElQIFNBUlZFIiwib21zIjoiSzEiLCJoc21fa2V5IjoiZjk3YmNjODgyZWM5MWUxNDA5NTU3NWE2NGM5MmQ0M2Y4MDkzYmU0MDE5NmIzMGI2YTlmNDU2MWIiLCJmeV9pZCI6IlhLMDMwNjEiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.-wbLMrxX-PaXalAHapE6MUfR29tYmdtHzP8QgnG5CW0'




def get_tradebook_sync(client_id: str, access_token: str):
    """
    Synchronously retrieves trade book information from the Fyers API.

    Args:
        client_id (str): Your Fyers API client ID.
        access_token (str): Your Fyers API access token.

        
    Returns:
        dict: Parsed trade book information.
    """
    try:
        # Initialize the FyersModel instance with async mode disabled (synchronous)
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

        # Make a synchronous request to get the trade book information
        response = fyers.tradebook()


        # Check if the response indicates success
        if response.get("s") == "ok":
            trade_book = response.get("tradeBook", [])
            trades = []

            # Iterate over each trade detail in 'tradeBook'
            for trade in trade_book:
                # Extract desired fields
                trade_info = {
                    'Client ID': trade.get('clientId', 'N/A'),
                    'Exchange': trade.get('exchange', 'N/A'),
                    'FY Token': trade.get('fyToken', 'N/A'),
                    'Order Number': trade.get('orderNumber', 'N/A'),
                    'Exchange Order No': trade.get('exchangeOrderNo', 'N/A'),
                    'Trade Number': trade.get('tradeNumber', 'N/A'),
                    'Trade Price': trade.get('tradePrice', 'N/A'),
                    'Segment': trade.get('segment', 'N/A'),
                    'Product Type': trade.get('productType', 'N/A'),
                    'Traded Quantity': trade.get('tradedQty', 'N/A'),
                    'Symbol': trade.get('symbol', 'N/A'),
                    'Row': trade.get('row', 'N/A'),
                    'Order DateTime': trade.get('orderDateTime', 'N/A'),
                    'Trade Value': trade.get('tradeValue', 'N/A'),
                    'Side': 'Buy' if trade.get('side') == 1 else 'Sell',
                    'Order Type': trade.get('orderType', 'N/A'),
                    'Order Tag': trade.get('orderTag', 'N/A')
                }
                trades.append(trade_info)

            # Convert the list of trades to a DataFrame for better presentation
            df_trades = pd.DataFrame(trades)

            print("\nTrade Book Information:")
            print(df_trades)

            # Optionally, export the trade book to an Excel file
            export_to_excel = input("\nWould you like to export the trade book to Excel? (y/n): ").strip().lower()
            if export_to_excel == 'y':
                excel_filename = "trade_book.xlsx"
                df_trades.to_excel(excel_filename, index=False, engine='openpyxl')
                print(f"Trade book successfully exported to {excel_filename}")
            else:
                print("Export to Excel skipped.")

            return df_trades

        else:
            print("\nFailed to retrieve trade book data.")
            print("Response:", response)
            return {}

    except Exception as e:
        print(f"\nAn error occurred while fetching trade book data: {e}")
        return {}

def main():
    """
    Entry point for the script.
    """
    # Validate credentials
    if CLIENT_ID == "YOUR_CLIENT_ID" or ACCESS_TOKEN == "YOUR_ACCESS_TOKEN":
        print("Please replace 'YOUR_CLIENT_ID' and 'YOUR_ACCESS_TOKEN' with your actual Fyers API credentials.")
        sys.exit(1)

    # Fetch and process trade book data
    get_tradebook_sync(CLIENT_ID, ACCESS_TOKEN)

if __name__ == "__main__":
    main()
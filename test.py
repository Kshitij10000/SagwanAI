import asyncio
from fyers_apiv3 import fyersModel  # Ensure this is the correct import based on the Fyers API documentation

# Replace these with your actual credentials
CLIENT_ID = "Y25P4GTMHA-100"
ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MjgzMDM1NzUsImV4cCI6MTcyODM0NzQzNSwibmJmIjoxNzI4MzAzNTc1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbkE5SFhXOGx0d3JYdVRfTFAteTJRTkxWSWpkV1UyTUpoZEp5WW5lV1hJZEI5N1hKb29mSFRON002Q0d4TFBqOEgzNGpDLUVVU1FLNThfc2JYeVRpTm1vOTRuX0t6VnJPRndwUzA0M1MzbUlGM1RoND0iLCJkaXNwbGF5X25hbWUiOiJLU0hJVElKIERJTElQIFNBUlZFIiwib21zIjoiSzEiLCJoc21fa2V5IjoiZjk3YmNjODgyZWM5MWUxNDA5NTU3NWE2NGM5MmQ0M2Y4MDkzYmU0MDE5NmIzMGI2YTlmNDU2MWIiLCJmeV9pZCI6IlhLMDMwNjEiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.-wbLMrxX-PaXalAHapE6MUfR29tYmdtHzP8QgnG5CW0'

async def get_funds_async(client_id: str, access_token: str):
    """
    Asynchronously retrieves funds information from the Fyers API.

    Args:
        client_id (str): Your Fyers API client ID.
        access_token (str): Your Fyers API access token.
    """
    try:
        # Initialize the FyersModel instance with async mode enabled
        fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=True, log_path="")

        # Make an asynchronous request to get the funds information
        response = await fyers.funds()

        # # Debug: Print the raw response
        # print("Raw Response:", response)

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

            print("\nFunds Information:")
            print(f"Total Balance: {total_balance}")
            print(f"Available Balance: {available_balance}")
            print(f"Utilized Amount: {utilized_amount}")
            print(f"Clear Balance: {clear_balance}")
            # Print other desired fields
        else:
            print("\nFailed to retrieve funds data.")
            print("Response:", response)

    except Exception as e:
        print(f"\nAn error occurred while fetching funds: {e}")

def main():
    """
    Entry point for the script.
    """
    asyncio.run(get_funds_async(CLIENT_ID, ACCESS_TOKEN))

if __name__ == "__main__":
    main()
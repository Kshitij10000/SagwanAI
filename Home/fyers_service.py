# Home/fyers_service.py
from urllib.parse import urlencode
from fyers_apiv3 import fyersModel 
from django.utils import timezone
from asgiref.sync import async_to_sync

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

# Home/fyers_service.py
from urllib.parse import urlencode
from fyers_apiv3 import fyersModel 
from django.utils import timezone 

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



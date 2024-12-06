import requests
from requests.exceptions import Timeout, RequestException, HTTPError, ConnectionError

class API_Call_Sportradar:
    
    def __init__(self,endpoint):
        self.apikey = "?api_key=UkM9wmn3UNaJ4qaV7mn0jzEcY8dJaFYQtqiHl5c3"
        self.url = "https://api.sportradar.com/tennis/trial/v3/en/" + endpoint + self.apikey

    
    def call_api(self):
        headers = {"accept": "application/json"}
        try:
            response = requests.get(self.url, headers=headers,timeout=30)
            response.raise_for_status()
            return response
        except Timeout:
            print("The request timed out. Please try again later.")
        except ConnectionError:
            print("Failed to connect to the API. Check your network connection.")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
            print(f"A request error occurred: {req_err}")
        except ValueError as json_err:
            print(f"Error parsing response data: {json_err}")
        except Exception as err:
            print(f"An unexpected error occurred: {err}")
        finally:
            print("API call completed.")


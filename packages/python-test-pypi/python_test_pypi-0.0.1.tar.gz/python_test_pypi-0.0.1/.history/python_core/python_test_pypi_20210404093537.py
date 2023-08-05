from python_core.exceptions.exceptions import HttpResponseException
import requests
import sys


class HttpEndpoint:
    """
    HttpEndpoint class, one instance per endpoint, offers get/post HTTP methods
    and handles both HTTP errors and API errors
    """    
    

    def __init__(self, endpoint_subdomain, global_req_params):
        """
        HttpEndpoint class, one instance per endpoint, offers get/post HTTP methods
        and handles both HTTP errors and API errors

        Args:
            endpoint (string): endpoint URL
            global_req_params (dict): dict of global params included in each request 
        """        
        
        self.endpoint_subdomain = endpoint_subdomain
        self.endpoint = f"https://{endpoint_subdomain}.abstractapi.com/v1/"
        self.global_req_params = global_req_params

    
    def get(self, req_params):
        """
        Make a get request to the endpoint

        Args:
            req_params (dict): dict of params included in this request
        """   

        # requests raises only connection related exceptions, unless exlicitly 
        # configured to raise Http exceptions
        try:     
            response = requests.get(
                url=self.endpoint,
                params={
                    **self.global_req_params,
                    **req_params
                }
            )
        except requests.exceptions.RequestException as req_exc:

            # RequestExceptions are expressive: ConnectionError, ConnectTimeout, InvalidURL, InvalidHeader 
            raise SystemExit(sys.exc_info())

        if response.ok:
            result = response.json()
            return result
        else:
            raise HttpResponseException(response.status_code)


    def post(self, payload, req_params):
        """
        Make a post request to the endpoint

        Args:
            payload (dict): post method payload
            req_params (dict): dict of params included in this request
        """        
        pass
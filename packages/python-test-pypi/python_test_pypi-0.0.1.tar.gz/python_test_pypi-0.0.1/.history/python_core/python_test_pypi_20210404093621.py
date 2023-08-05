from python_core.exceptions.exceptions import HttpResponseException
import requests
import sys


class HttpTestPyPi:
    """
    HttpTestPyPi class
    """    
    

    def __init__(self):
        """
        HttpTestPyPi class 
        """        

    
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
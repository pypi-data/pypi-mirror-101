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

    
    def get(self, req_params=None):
        """
        Make a get request
        """   

        return "hi"


    def post(self, payload, req_params):
        """
        Make a post request
        """        
        return "hi post"
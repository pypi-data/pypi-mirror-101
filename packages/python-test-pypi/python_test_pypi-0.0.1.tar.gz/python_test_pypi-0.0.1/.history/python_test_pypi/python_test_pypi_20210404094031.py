from python_test_pypi.exceptions.exceptions import HttpExceptionTest
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

        return "hi get"


    def post(self, payload, req_params):
        """
        Make a post request
        """        
        raise HttpExceptionTest()
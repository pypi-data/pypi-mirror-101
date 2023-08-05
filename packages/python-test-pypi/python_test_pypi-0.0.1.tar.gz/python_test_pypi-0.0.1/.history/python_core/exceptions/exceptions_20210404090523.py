class HttpResponseException(Exception):
    """
    An Exception caused by bad Http response code
    Http codes >= 400
    """    

    def __init__(self, http_code, msg):
        """
        An Exception caused by bad Http response code
        Http codes >= 400

        Args:
            http_code (int): http response status code that caused the error,
                             will determine the type of exception message
        """        
        self.http_code = http_code
        self.msg = msg
    
    def __str__(self):
        output = f"""
            [ HttpResponseException ]
            {self.http_code} -- {self.msg}
        """

        return output


class APIException(Exception):
    """
    An Exception caused by an API response with
    an error, the recieved error message/description
    will be raised
    """    

    def __init__(self, http_code, msg):
        """
        An Exception caused by an API response with
        an error, the recieved error message/description
        will be raised

        Args:
            response (dict): the response as json, will be parsed here
        """        
        pass
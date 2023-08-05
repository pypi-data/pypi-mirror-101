class HttpException(Exception):
    """
    An Exception
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
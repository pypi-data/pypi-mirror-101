class HttpException(Exception):
    """
    An Exception
    """    

    def __init__(self, http_code, msg):
        """
        An Exception
        """        
        self.http_code = http_code
        self.msg = msg
    
    def __str__(self):
        output = f"""
            [ HttpResponseException ]
            {self.http_code} -- {self.msg}
        """

        return output
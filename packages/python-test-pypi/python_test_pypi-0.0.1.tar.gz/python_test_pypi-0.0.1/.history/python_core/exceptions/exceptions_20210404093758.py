class HttpException(Exception):
    """
    An Exception
    """    

    def __init__(self):
        """
        An Exception
        """        
        self.http_code = 400
        self.msg = "http msg"
    
    def __str__(self):
        output = f"""
            [ HttpResponseException ]
            {self.http_code} -- {self.msg}
        """

        return output
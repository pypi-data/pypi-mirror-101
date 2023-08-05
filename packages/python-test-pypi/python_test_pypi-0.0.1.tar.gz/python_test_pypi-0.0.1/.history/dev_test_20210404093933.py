from python_core import HttpEndpoint
from python_core.exceptions import HttpResponseException, APIException


api = HttpEndpoint()
result = api.get()
print("\nresult : ",result)
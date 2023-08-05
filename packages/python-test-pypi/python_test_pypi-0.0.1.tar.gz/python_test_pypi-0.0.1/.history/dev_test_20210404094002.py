from python_test_pypi import HttpEndpoint
from python_test_pypi.exceptions import HttpResponseException, APIException


api = HttpEndpoint()
result = api.get()
print("\nresult : ",result)
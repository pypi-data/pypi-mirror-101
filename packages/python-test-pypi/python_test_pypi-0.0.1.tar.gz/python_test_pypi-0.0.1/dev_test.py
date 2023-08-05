from python_test_pypi import HttpTestPyPi
from python_test_pypi.exceptions import HttpExceptionTest


api = HttpTestPyPi()
result = api.get()
print("\nresult : ",result)
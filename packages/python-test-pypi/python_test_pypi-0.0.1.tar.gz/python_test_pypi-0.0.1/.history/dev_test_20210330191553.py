from python_core import HttpEndpoint
from python_core.exceptions import HttpResponseException, APIException


api = HttpEndpoint(
    "ipgeolocation",
    global_req_params={"lang":"python"}
    )

result = api.get({
    "api_key" : "2f2fddad79404b90bf7c180cf3368bd0"
})

print("\nresult : ",result)
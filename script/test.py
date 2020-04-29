from __future__ import print_function
from swagger_client.rest import ApiException
import time
import swagger_client
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.AuthenticationApi()
body = {"username": "Blue","password": "n96{ZYV7"}
 # Login | Authenticate by username and password
contentType = contentType_example # String | Specify the data Content-Type
print()
try: 
    # Login
    api_response = api_instance.login(body, contentType)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AuthenticationApi->login: %s\n" % e)
# Beginning of Klarna code base

The ```klarna_api``` code base is very low level usage of the existing API to create sessison, and generate/manage orders.

__NOTE__: The ```klarna_api``` code takes advantage of the ```requests``` library for Python. 

_Also Note_: To obtain an authorization token to generate an order will require using the Klarna SDK.

### Config setup
While not required, I prefer configuration setups when possible. To use the code as it you would need a ```~/.ssh/klarna_api.json``` file. 
The general file setup is:

{
"headers": {"Content-type":"application/json", "Accept":"application/json"},
"user_id": "your user id",
"password": "your password",
"base_url": "https://api-na.playground.klarna.com"
}

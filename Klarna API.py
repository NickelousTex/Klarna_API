import os
import sys
import json
import requests


# Reused variables
# converted to config based
with open('klarna_api.json') as json_file:
    config = json.load(json_file)
    BASE_URL = config['base_url']
    AUTHORIZATION = (config['user_id'], config['password'])
    HEADERS = config['headers']

# Wrapper methods to help generate usable output
def get_method(url, author=AUTHORIZATION, head=HEADERS):
    output = requests.get(url, auth=author, headers=head,  stream=True)
    output.raise_for_status()
    return json.loads(output.text)

def post_method(url, payload={}, authorize=AUTHORIZATION, head=HEADERS):
    if payload:
        output = requests.post(url, data=json.dumps(payload), auth=authorize, headers=head)
    else:
        output = requests.post(url, auth=authorize, headers=head)
    output.raise_for_status()
    if output.text:
        return json.loads(output.text)
    else:
        return output
        
# Mock payloads
instrument_example = {
  "locale": "en-US",
  "purchase_country": "US",
  "purchase_currency": "USD",
  "merchant_reference1": "my_customerorderID",
  "order_amount": 18000,
  "order_tax_amount": 2000,
  "order_lines": [
    {
      "reference": "KLN-100",
      "quantity": 1,
      "unit_price": 8000,
      "total_amount": 8000,
      "type": "instrument",
      "name": "bagpipe"
    },
    {
      "reference": "KLN-101",
      "quantity": 1,
      "unit_price": 8000,
      "total_amount": 8000,
      "type": "instrument",
      "name": "drums"
    },
    {
      "quantity": 1,
      "total_amount": 2000,
      "type": "sales_tax",
      "name": "Tax",
      "unit_price": 2000
    }
  ]
}

klarna_example = {
  "locale": "en-US",
  "purchase_country": "US",
  "purchase_currency": "USD",
  "merchant_reference1": "Klarna_customerorderID",
  "order_amount": 18000,
  "order_tax_amount": 2000,
  "order_lines": [
    {
      "reference": "KLN-100",
      "quantity": 1,
      "unit_price": 8000,
      "image_url": "https://www.klarna.com/example/image/prod.jpg",
      "total_amount": 8000,
      "type": "physical",
      "product_url": "https://www.klarna.com/example/widget1=prod",
      "name": "Klarna Widget 1"
    },
    {
      "reference": "KLN-101",
      "quantity": 1,
      "unit_price": 8000,
      "image_url": "https://www.klarna.com/example/image/prod.jpg",
      "total_amount": 8000,
      "type": "physical",
      "product_url": "https://www.klarna.com/example/widget2=prod",
      "name": "Klarna Widget 2"
    },
    {
      "quantity": 1,
      "total_amount": 2000,
      "type": "sales_tax",
      "name": "Tax",
      "unit_price": 2000
    }
  ]
}


### SESSION ###
# Create a new session
session = post_method('{}/payments/v1/sessions'.format(BASE_URL),  
                       payload=klarna_example)

# Realize we can get the client token right here, but want to work on get method
session_id = session['session_id']


# GET SESSION
session = get_method('{}/payments/v1/sessions/{}'.format(BASE_URL, session_id))
print(session)



# UPDATE STATUS
status_update = post_method('{}/payments/v1/sessions/{}'.format(BASE_URL, session_id), 
                              payload=instrument_purchase)
#
##
### Drop session info into SDK on client side, finish process and retrieve authorization token
##
#



### ORDERS MANAGEMENT ###

# CREATE ORDER:
AUTHORIZATION_TOKEN = ''  # obtained via client side
order_create = post_method('{}/payments/v1/authorizations/{}/order'.format(BASE_URL, AUTHORIZATION_TOKEN),
                          payload=klarna_example)


# CANCEL ORDER (Note can not be done once order is captured)
order_canceled = requests.post('https://api-na.playground.klarna.com/ordermanagement/v1/orders/{}/cancel'.format('52bcaca0-35bb-2c78-90b4-baa99199cd80'), 
                       auth=('N104701_f720721d7d66', 'uEWwK2Ziu2pZKdk1'), 
                       headers=HEADERS)

# just a reminder that we have the order id from creation
order_create['order_id']


# GET ORDER
get_order = get_method('{}/ordermanagement/v1/orders/{}'.format(BASE_URL, order_create['order_id']))


# ACKNOWLEDGE ORDER
acknowledge_order = post_method('{}/ordermanagement/v1/orders/{}/acknowledge'.format(BASE_URL, 
                                                                                    order_create['order_id']))


# CAPTURE ORDER
capture_payload = {
    "captured_amount": 18000,
    "description": "captured",
    "reference": "for this id"
}

capture_order = post_method('{}/ordermanagement/v1/orders/{}/captures'.format(BASE_URL,
                                                                              order_create['order_id']),
                                                                              payload=capture_payload)

# REFUND ORDER
refund_info = {
    "refunded_amount": 400
}
refunded = post_method('{}/ordermanagement/v1/orders/{}/refunds'.format(BASE_URL, order_create['order_id']),
                        payload=refund_info)

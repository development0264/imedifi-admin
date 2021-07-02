from paypalpayoutssdk.core import PayPalHttpClient, SandboxEnvironment
from paypalpayoutssdk.payouts import PayoutsPostRequest
from paypalhttp import HttpError


# Creating Access Token for Sandbox
client_id = "AUP9E4-uvz3Tx6ux-uTQiWgnsjQKITrHwVxj_SBJIDDvp2d4j1GYJPR9A6QYzgFCC5Dtj56N2LD11jbA"
client_secret = "EEq-jVAOlPun-7gaRtFpzOVhpDIngh1AlaHlBQXVAlaY6I92bPlyVFYw600tD621AfWvFv8rtgheexCs"
# Creating an environment
environment = SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(environment)
print(client)

# Construct a request object and set desired parameters
# Here, PayoutsPostRequest()() creates a POST request to /v1/payments/payouts
body = {
    "sender_batch_header": {
        "recipient_type": "EMAIL",
        "email_message": "SDK payouts test txn",
        "note": "Enjoy your Payout!!",
        "sender_batch_id": "Test_SDK_1",
        "email_subject": "This is a test transaction from SDK"
    },
    "items": [{
        "note": "Your 5$ Payout!",
        "amount": {
            "currency": "USD",
            "value": "1.00"
        },
        "receiver": "payout-sdk-1@paypal.com",
        "sender_item_id": "Test_txn_1"
    }, {
        "note": "Your 5$ Payout!",
        "amount": {
            "currency": "USD",
            "value": "1.00"
        },
        "receiver": "payout-sdk-2@paypal.com",
        "sender_item_id": "Test_txn_2"
    }, {
        "note": "Your 5$ Payout!",
        "amount": {
            "currency": "USD",
            "value": "1.00"
        },
        "receiver": "payout-sdk-3@paypal.com",
        "sender_item_id": "Test_txn_3"
    }, {
        "note": "Your 5$ Payout!",
        "amount": {
            "currency": "USD",
            "value": "1.00"
        },
        "receiver": "payout-sdk-4@paypal.com",
        "sender_item_id": "Test_txn_4"
    }, {
        "note": "Your 5$ Payout!",
        "amount": {
            "currency": "USD",
            "value": "1.00"
        },
        "receiver": "payout-sdk-5@paypal.com",
        "sender_item_id": "Test_txn_5"
    }]
}

request = PayoutsPostRequest()
request.request_body (body)

try:
    # Call API with your client and get a response for your call
    response = client.execute(request)
    # If call returns body in response, you can get the deserialized version from the result attribute of the response
    batch_id = response.result.batch_header.payout_batch_id
    print(batch_id)        
except IOError as ioe:
    print(ioe)
    if isinstance(ioe, HttpError):
        # Something went wrong server-side
        print(ioe.status_code)
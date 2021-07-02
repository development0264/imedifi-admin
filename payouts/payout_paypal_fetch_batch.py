from paypalpayoutssdk.payouts import PayoutsGetRequest
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

# Here, PayoutsGetRequest() creates a GET request to /v1/payments/payouts/<batch-id>
request = PayoutsGetRequest("HTS8J2372W82G")

try:
    # Call API with your client and get a response for your call
    response = client.execute(request)

    # If call returns body in response, you can get the deserialized version from the result attribute of the response
    batch_status = response.result.batch_header.batch_status
    print(response.result)
except IOError as ioe:
    if isinstance(ioe, HttpError):
        # Something went wrong server-side
        print(ioe.status_code)
        print(ioe.headers)
        print(ioe)
    else:
        # Something went wrong client side
        print(ioe)

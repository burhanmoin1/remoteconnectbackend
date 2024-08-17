from square.http.auth.o_auth_2 import BearerAuthCredentials
from square.client import Client

# Initialize the Square Client
SQUARE_ACCESS_TOKEN = 'EAAAl4sXUPYME1zFo99Y5lye0L67g9PRsGWlTtSLL7pQDk4rWg8ffd2JWjiwQgVf'
SQUARE_ENVIRONMENT = 'sandbox'

client = Client(
    bearer_auth_credentials=BearerAuthCredentials(
        access_token=SQUARE_ACCESS_TOKEN
    ),
    environment='sandbox')

# Get the Payments API
payments_api = client.payments

# Create a payment
def create_payment():
    body = {
        "source_id": "cnon:card-nonce-ok",  # Replace with a valid source_id from your Square integration
        "idempotency_key": "1f3b959d-ec47-492e-9b1c-e180db1cf1f4",
        "amount_money": {
            "amount": 100,  # Amount in cents ($1.00)
            "currency": "USD"
        },
        "location_id": "L3G9Z30R27SS3"  # Replace with your valid location_id
    }

    result = payments_api.create_payment(body)

    if result.is_success():
        print("Payment created successfully:")
        print(result.body)
    elif result.is_error():
        print("Error creating payment:")
        print(result.errors)

# Call the function
create_payment()

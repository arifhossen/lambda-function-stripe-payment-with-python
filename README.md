# Lambda Function -> Stripe Card Payment Integration with Python

* Stripe Card Payment like VISA, MASTER CARD, AMERICAN EXPRESS, etc..

## Step 1: Create New Python Project
* At first need to create your python project and then follow the guideline step by step.

## Step 2: Stripe Python Package Installation

```python
pip install stripe
```

## Step 3: Create Your Lambda Function File
```python
File Name: lambda_function.py
```

## Step 4: Write Your Lambda Function Code

```python
import requests
import json
import stripe


def lambda_handler(event, context):

    resource = event.get("resource")
    method = event.get("httpMethod")

    if resource == '/payment/stripe/gettoken':
        if method == 'POST':
            event_body = event.get("body")
            json_data = json.loads(event_body)
            result = get_token(json_data)
        else:

            data = {"message": "Method Not Allowed"}
            result = {'statusCode': 405, 'body': json.dumps(data)}

    elif resource == '/payment/stripe/cardpayment':
        if method == 'POST':
            event_body = event.get("body")
            json_data = json.loads(event_body)
            result = card_payment(json_data)
        else:

            data = {"message": "Method Not Allowed"}
            result = {'statusCode': 405, 'body': json.dumps(data)}
    else:
        data = {"message": "Resource Not Allowed"}
        result = {'statusCode': 405, 'body': json.dumps(data)}

    response_headers = {
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
        }
    }

    result.update(response_headers)
    return result


def get_token(data):

    try:
        stripe.api_key = "sk_test_YOUR_API_KEY_HERE"
        card_info = data["card_info"]
        token_response = stripe.Token.create(
            card={
                "number": card_info["card_number"],
                "exp_month": card_info["card_expiry_month"],
                "exp_year": card_info["card_expiry_year"],
                "cvc": card_info["card_cvc"],
            },
        )

        if 'id' in token_response:
            token_object = {"tok_card": token_response["id"]}
            result = {'status': True, "message": "Stripe Token Get Successfully",
                      "result": token_object
                      }
        else:
            result = {'status': False, "message": "Stripe Token Generate Failure",
                      "result": token_response}
        return {'statusCode': 200, 'body': json.dumps(result)}

    except Exception as e:
        result = {'status': False, "message": "Stripe Card Payment Transaction Failure", "error": e}
        return {'statusCode': 401, 'body': json.dumps(result)}

def card_payment(data):

    try:
        stripe.api_key = "sk_test_YOUR_API_KEY_HERE"
        charge_response = stripe.Charge.create(
            amount=data["amount"],
            currency=data["currency"],
            card=data["tok_card"],
            description= data["description"],
            metadata={'order_id':  data["order_id"]}

        )

        if 'id' in charge_response:
            result = {'status': True, "message": "Stripe Card payment transaction success",
                      "result": charge_response
                      }
            return {'statusCode': 200, 'body': json.dumps(result)}
        else:

            result = {'status': True, "message": "Stripe Card payment transaction Failure","result": charge_response}
            return {'statusCode': 200, 'body': json.dumps(result)}

    except Exception as e:
        print(e)
        result = {'status': False, "message": "Stripe Card Payment Transaction Failure"}
        return {'statusCode': 401, 'body': json.dumps(result)}





```

## Step 5: API Request URL with Body JSON Data For Get  tok_card

* {{url}}/payment/stripe/gettoken
* Method: POST

```python
{
    "card_info": {
        "card_type": "VISA",
        "card_number": "378282246310005",
        "card_expiry_month": "10",
        "card_expiry_year": "21",
        "card_cvc": "123",
        "cardholder_name": "Arif Hossen"
    }
}

```

## Step 6: Card Token Reponse Data

```python
{
    "status": true,
    "message": "Stripe Token Get Successfully",
    "result": {
        "tok_card": "tok_1GlrQwEmyhTFDlRB3V1bw3ML"
    }
}
```


## Step 7: API Request URL with Body JSON Data For Card Transaction

* {{url}}/payment/stripe/cardpayment
* Method: POST

```python
{
    "amount": "7800",
    "currency": "usd",
    "tok_card": "tok_1Gla13EmyhTFDlRB69NJjeYd",
    "description": "KhaoDao Payment From Moby Dick Restaurant",
    "cardholder_name": "Arif Hossen",
    "order_id": "1002"
}

```

## Step 8: Card Transaction Output Reponse Data

```python
{
    "status": true,
    "message": "Stripe Card payment transaction success",
    "result": {
        "id": "ch_1GlrUlEmyhTFDlRB17d4urU6",
        "object": "charge",
        "amount": 7800,
        "amount_refunded": 0,
        "application": null,
        "application_fee": null,
        "application_fee_amount": null,
        "balance_transaction": "txn_1GlrUlEmyhTFDlRByvJ4eFFS",
        "billing_details": {
            "address": {
                "city": null,
                "country": null,
                "line1": null,
                "line2": null,
                "postal_code": null,
                "state": null
            },
            "email": null,
            "name": null,
            "phone": null
        },
        "calculated_statement_descriptor": "Stripe",
        "captured": true,
        "created": 1590217811,
        "currency": "usd",
        "customer": null,
        "description": "Beta Transaction",
        "destination": null,
        "dispute": null,
        "disputed": false,
        "failure_code": null,
        "failure_message": null,
        "fraud_details": {},
        "invoice": null,
        "livemode": false,
        "metadata": {
            "order_id": "1002"
        },
        "on_behalf_of": null,
        "order": null,
        "outcome": {
            "network_status": "approved_by_network",
            "reason": null,
            "risk_level": "normal",
            "risk_score": 36,
            "seller_message": "Payment complete.",
            "type": "authorized"
        },
        "paid": true,
        "payment_intent": null,
        "payment_method": "card_1GlrUcEmyhTFDlRBhXYA08Vn",
        "payment_method_details": {
            "card": {
                "brand": "amex",
                "checks": {
                    "address_line1_check": null,
                    "address_postal_code_check": null,
                    "cvc_check": "pass"
                },
                "country": "US",
                "exp_month": 10,
                "exp_year": 2021,
                "fingerprint": "sy7N3Y5O6mA93lU6",
                "funding": "credit",
                "installments": null,
                "last4": "0005",
                "network": "amex",
                "three_d_secure": null,
                "wallet": null
            },
            "type": "card"
        },
        "receipt_email": null,
        "receipt_number": null,
        "receipt_url": "https://pay.stripe.com/receipts/acct_1GlVTOEmyhTFDlRB/ch_1GlrUlEmyhTFDlRB17d4urU6/rcpt_HKWXsDmDPHAJMOK7Y2GFmlAx4gwlF00",
        "refunded": false,
        "refunds": {
            "object": "list",
            "data": [],
            "has_more": false,
            "total_count": 0,
            "url": "/v1/charges/ch_1GlrUlEmyhTFDlRB17d4urU6/refunds"
        },
        "review": null,
        "shipping": null,
        "source": {
            "id": "card_1GlrUcEmyhTFDlRBhXYA08Vn",
            "object": "card",
            "address_city": null,
            "address_country": null,
            "address_line1": null,
            "address_line1_check": null,
            "address_line2": null,
            "address_state": null,
            "address_zip": null,
            "address_zip_check": null,
            "brand": "American Express",
            "country": "US",
            "customer": null,
            "cvc_check": "pass",
            "dynamic_last4": null,
            "exp_month": 10,
            "exp_year": 2021,
            "fingerprint": "sy7N3Y5O6mA93lU6",
            "funding": "credit",
            "last4": "0005",
            "metadata": {},
            "name": null,
            "tokenization_method": null
        },
        "source_transfer": null,
        "statement_descriptor": null,
        "statement_descriptor_suffix": null,
        "status": "succeeded",
        "transfer_data": null,
        "transfer_group": null
    }
}
```

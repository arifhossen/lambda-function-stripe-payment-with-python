import requests
import json
import stripe


def lambda_handler(event, context):

    resource = event.get("resource")
    method = event.get("httpMethod")

    if resource == '/stripe/gettoken':
        if method == 'POST':
            event_body = event.get("body")
            json_data = json.loads(event_body)
            result = get_token(json_data)
        else:

            data = {"message": "Method Not Allowed"}
            result = {'statusCode': 405, 'body': json.dumps(data)}

    elif resource == '/stripe/cardpayment':
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



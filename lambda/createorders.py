import json
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('blueocean-orders') #tablename

sqs = boto3.client('sqs')

QUEUE_URL = "YOUR_QUEUE_URL"

def lambda_handler(event, context):

    try:

        body = json.loads(event['body'])

        customer_name = body['customerName']
        customer_email = body['customerEmail']
        product_name = body['productName']
        quantity = body['quantity']

        order_id = str(uuid.uuid4())

        order = {
            'orderId': order_id,
            'customerName': customer_name,
            'customerEmail': customer_email,
            'productName': product_name,
            'quantity': quantity,
            'status': 'PLACED'
        }

        table.put_item(Item=order)

        sqs.send_message(
            QueueUrl= QUEUE_URL,
            MessageBody=json.dumps(order)
        )

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Order Created Successfully',
                'orderId': order_id
            })
        }

    except Exception as e:

        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(str(e))
        }

import json
import os
import boto3
from boto3.dynamodb.conditions import Attr


TABLE_NAME = os.environ["TABLE_NAME"]
table = boto3.resource("dynamodb").Table(TABLE_NAME)




def lambda_handler(event, context):
	"""Handle GET requests and return all orders or orders for one email."""
	
	params = event.get("queryStringParameters") or {}
	customer_email = params.get("customerEmail")

	scan_args = {}
	if customer_email:
		scan_args["FilterExpression"] = Attr("customerEmail").eq(customer_email)

	items = []
	while True:
		response = table.scan(**scan_args)
		items.extend(response.get("Items", []))
		last_key = response.get("LastEvaluatedKey")
		if not last_key:
			break
		scan_args["ExclusiveStartKey"] = last_key

	return {
		"statusCode": 200,
		"headers": {"Content-Type": "application/json"},
		"body": json.dumps(items, default=str),
	}

# Example Lambda test event: omit or set ``queryStringParameters`` to ``None``
# to return all orders.
#TEST_EVENT = {
#	"queryStringParameters": {
#		"customerEmail": "customer@example.com"
#	}
#}

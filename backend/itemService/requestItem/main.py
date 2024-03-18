import boto3
import json
import time
from decimal import Decimal

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb', region_name='ca-central-1')
    table = dynamodb.Table(table_name)
    return table

def parse_event_body(event_body):
    """Parse the event body, converting from JSON string to dictionary if necessary."""
    if isinstance(event_body, str):
        return json.loads(event_body)
    return event_body

def decimal_default(obj):
    """Convert Decimal objects to float. Can be passed as the 'default' parameter to json.dumps()."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def update_borrow_requests(table, itemID, data):
    current_data = table.get_item(Key={'itemID': itemID})
    borrow_requests = current_data.get('Item', {}).get('borrowRequests', [])

    for request in borrow_requests:
        if request['borrowerID'] == data['borrowerID']:
            request.update(data)
            break
    else:
        borrow_requests.append(data)

    response = table.update_item(
        Key={'itemID': itemID},
        UpdateExpression="SET borrowRequests = :br",
        ExpressionAttributeValues={':br': borrow_requests},
        ReturnValues="UPDATED_NEW"
    )
    return response


def handler(event, context):
    try:
        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        body = parse_event_body(event["body"])
        itemID = body["itemID"]
        borrowerID = body["borrowerID"]
        timestamp = Decimal(time.time())
        startDate = body["startDate"]
        endDate = body["endDate"]

        if startDate > endDate:
            raise ValueError("startDate cannot be after endDate")

        data = {
            "borrowerID": borrowerID,
            "timestamp": timestamp,
            "startDate": startDate,
            "endDate": endDate
        }

        response = update_borrow_requests(table, itemID, data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'BorrowerID appended successfully',
                'updatedAttributes': response['Attributes']
            }, default=decimal_default)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

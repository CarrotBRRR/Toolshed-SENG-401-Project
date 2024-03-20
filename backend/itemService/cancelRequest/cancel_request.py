import boto3
import json

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

def set_borrower_to_borrow_requests(table, itemID, data):
    """Append a borrowerID to the borrowRequests array in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="SET borrowRequests = :b",
        ExpressionAttributeValues={
            ':b': data
        },
        ReturnValues="UPDATED_NEW"
    )
    return response

def delete_borrow_request_array(table, itemID):
    """Delete a borrowerID from the borrowRequests array in the DynamoDB table."""
    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="REMOVE borrowRequests",
        ReturnValues="UPDATED_NEW"
    )
    return response

def move_borrow_request_to_past_requests(table, itemID, data):
    """Move a borrow request to the pastRequests array in the DynamoDB table."""
    item = table.get_item(Key={'itemID': itemID})
    borrow_requests = item.get('Item', {}).get('pastRequests', [])

    borrow_requests.append(data)

    response = table.update_item(
        Key={
            'itemID': itemID
        },
        UpdateExpression="SET pastRequests = :br",
        ExpressionAttributeValues={
            ':b': data
        },
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

        item = table.get_item(
            Key={
                'itemID': itemID
            }
        )

        if 'Item' not in item:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': f'Item {itemID} not found'
                })
            }
        
        if 'borrowRequests' not in item['Item']:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': f'Item {itemID} has no borrowRequests'
                })
            }
        
        else:
            borrowRequests = item['Item']['borrowRequests']

        requests = []
        cancelled = []
        for request in borrowRequests:
            if request['borrowerID'] != borrowerID:
                requests.append(request)
            else:
                cancelled.append(request)

        if cancelled == []:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'BorrowerID not found in borrowRequests'
                })
            }
        
        else:
            if requests == []:
                response = delete_borrow_request_array(table, itemID)

            else:
                response = set_borrower_to_borrow_requests(table, itemID, requests)

            cancelled_request = {
                'request': cancelled,
                'status': 'cancelled'
            }

            response2 = move_borrow_request_to_past_requests(table, itemID, cancelled)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'BorrowerID removed successfully',
                    'updatedAttributes': json.dumps([response, response2])
                })
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': str(e)
            })
        }
import boto3
import requests
import json
import uuid
import hashlib
import base64
import time
from decimal import Decimal
import os

def get_dynamodb_table(table_name):
    """Initialize a DynamoDB resource and get the table."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    return table

def parse_event_body(event_body):
    """Parse the event body, converting from JSON string to dictionary if necessary."""
    if isinstance(event_body, str):
        return json.loads(event_body)
    return event_body

def insert_item_in_table(table, data):
    """Insert an item into the DynamoDB table."""
    response = table.put_item(
        Item=data,
        ReturnValues='ALL_OLD'
    )
    return response

def post_image(image, timestamp):
    # Get the credentials from AWS Parameter Store
    ssm = boto3.client('ssm')
    parameter_names = []
    key_string = ssm.get_parameter(
        Name="CloudinaryKey",
        WithDecryption=True
    )["Parameter"]["Value"]

    keys = key_string.split(",")

    cloud_name = keys[0]
    api_key = keys[1]
    api_secret = keys[2]

    # Set up the URL
    url = f'https://api.cloudinary.com/v1_1/{cloud_name}/image/upload/'

    # Set up the payload
    payload = {
        'api_key': api_key,
        'timestamp': timestamp
    }
    file = {
        'file': image
    }

    # Create a signature and add it to the payload
    payload["signature"] = create_signature(payload, api_secret)

    # Post the image to Cloudinary
    res = requests.post(url, files=file, data=payload)
    print(res.json())
    return res.json()

def create_signature(body, api_secret):
    exclude = ["api_key", "resource_type", "cloud_name"]
    sorted_body = sort_dict(body, exclude)
    query_string = create_query_string(sorted_body)
    query_string = f"{query_string}{api_secret}"
    hashed = hashlib.sha1(query_string.encode("utf-8")).hexdigest()
    return hashed

def sort_dict(dict, exclude):
    myKeys = list(dict.keys())
    myKeys.sort()
    for i in range(len(exclude)):
        if exclude[i] in myKeys:
            myKeys.remove(exclude[i])

    return {i: dict[i] for i in myKeys}

def create_query_string(dict):
    query_string = ""
    for ind, (key, value) in enumerate(dict.items()):
        query_string = f"{key}={value}" if ind == 0 else f"{query_string}&{key}={value}"
    return query_string

def handler(event, context):
    try:
        if os.environ.get('ENV') != 'testing':
            req = requests.get(f'https://www.googleapis.com/oauth2/v1/userinfo?access_token={header["token"]}',
                        headers={
                            "Authorization": f"Bearer {header['accesstoken']}",
                            "Accept": "application/json"
                        })
        
            if req.status_code != 200:
                return {
                "statusCode": 401,
                "body": json.dumps({"message": "Invalid user"})
                }
        # Parse the event body
        body = parse_event_body(event["body"])

        lenderID = body['lenderID']
        itemName = body['listingTitle']
        description = body['description']
        condition = body['condition']
        location = body['location']
        category = body['category']

        # Create a unique item ID
        itemID = str(uuid.uuid4())

        # Get the current time
        timestamp = Decimal(time.time())
        stringtime = str(timestamp)

        # Image handling
        raw_images = body['images']
        image_urls = []
        for raw_image in raw_images:
            if raw_image is not None and raw_image != "null":
                # Decode the image
                image_bytes = base64.b64decode(raw_image)

                # Save the image to a temp file
                filename = "/tmp/img.png"
                
                with open(filename, "wb") as f:
                    f.write(image_bytes)

                # Upload the image to Cloudinary
                with open(filename, "rb") as f:
                    image_urls.append(post_image(f, stringtime)["secure_url"])

        # Prepare the data to be inserted into the table
        data = {
            'itemID': itemID,
            'itemName': itemName,
            'condition': condition,
            'description': description,
            'category': category,
            'location': location,
            'images': image_urls,
            'lenderID': lenderID,
            'timestamp': timestamp
        }

        # Insert the item into the table
        table_name = 'items-30144999'
        table = get_dynamodb_table(table_name)
        response = insert_item_in_table(table, data)

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    
    except KeyError as ke:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": f"Missing required field: {str(ke)}"
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

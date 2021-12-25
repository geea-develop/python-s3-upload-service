import boto3
import os
from dotenv import load_dotenv

load_dotenv()

dynamodb = boto3.resource('dynamodb', endpoint_url=os.getenv("DYNAMODB_ENDPOINT", ""), region_name=os.getenv("DYNAMODB_REGION", "us-east-1"))

class Journal:
    def __init__(self, table_name = "Journal"):
        self.table_name = table_name
        self.client = dynamodb.Table(self.table_name)
        print(self.client.load())

    def get_record(self, PPK, PRK):
        response = self.client.get_item(
            Key={
                'PPK': PPK, 
                'PRK': PRK
                }
            )
        return response

    def put_record(self, PPK, PRK, data):
        print(f"Create record PPK={PPK} PRK={PRK}")
        response = self.client.put_item(
            Item={
                'PPK': PPK,
                'PRK': PRK,
                'data': data
                }
            )
        return response

    def update_record(self, PPK, PRK, key, value):
        print(f"Update record PPK={PPK} PRK={PRK} key={key}")
        response = self.client.update_item(
            Key={
                'PPK': PPK,
                'PRK': PRK,
            },
            UpdateExpression=f"set #k=:v",
            ExpressionAttributeValues={
                ':v': value,
            },
            ExpressionAttributeNames={
                '#k': key
            }
        )
        return response

    def delete_record(self, PPK, PRK):
        print(f"Delete record PPK={PPK} PRK={PRK}")
        response = self.client.delete_item(
            Key={
                'PPK': PPK,
                'PRK': PRK,
            }
        )
        return response

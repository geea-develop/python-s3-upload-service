from datetime import datetime
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer

class Journal:
    def __init__(self, client, table_name = "Journal"):
        self.table_name = table_name
        self.client = client
        # response = client.list_tables()
        # print(response)
        # print(self.client.load())

    def get_record(self, PPK, PRK):
        item_key = {
                'PPK': PPK,
                'PRK': PRK,
        }
        serializer = TypeSerializer()
        item_key = {k: serializer.serialize(v) for k,v in item_key.items()}
        response = self.client.get_item(
            TableName=self.table_name,
            Key=item_key
        )
        deserializer = TypeDeserializer()
        if response["Item"]:
            return {k: deserializer.deserialize(v) for k, v in response["Item"].items()}
        return None

    def put_record(self, PPK, PRK, data):
        print(f"Create record PPK={PPK} PRK={PRK}")
        item = {**{
                    'PPK': PPK,
                    'PRK': PRK
        }, **data}
        # To go from python to low-level format
        serializer = TypeSerializer()
        item = {k: serializer.serialize(v) for k,v in item.items()}
        response = self.client.put_item(
            TableName=self.table_name,
            Item=item
        )
        return response

    def update_record(self, PPK, PRK, key, value):
        print(f"Update record PPK={PPK} PRK={PRK} key={key}")
        item_key = {
                'PPK': PPK,
                'PRK': PRK,
        }
        serializer = TypeSerializer()
        item_key = {k: serializer.serialize(v) for k,v in item_key.items()}
        xprv = {
            ':v': value,
        }
        xprv = {k: serializer.serialize(v) for k,v in xprv.items()}
        response = self.client.update_item(
            TableName=self.table_name,
            Key=item_key,
            UpdateExpression=f"set #k=:v",
            ExpressionAttributeValues=xprv,
            ExpressionAttributeNames={
                '#k': key
            }
        )
        return response

    def delete_record(self, PPK, PRK):
        print(f"Delete record PPK={PPK} PRK={PRK}")
        item_key = {
                'PPK': PPK,
                'PRK': PRK,
        }
        serializer = TypeSerializer()
        item_key = {k: serializer.serialize(v) for k,v in item_key.items()}
        response = self.client.delete_item(
            TableName=self.table_name,
            Key=item_key
        )
        return response

    def list_records(self, PPK, PRK=None):
        print(f"List records PPK={PPK} PRK={PRK}")
        condition_expr = "#pkn = :pkv"
        xprv = {
                ':pkv': PPK
        }
        xprn = {
                '#pkn': 'PPK'
        }
        if PRK:
            xprv[':skv'] = PRK
            xprn['#skn'] = 'PRK'
            condition_expr = condition_expr + " AND #skn = :skv"
        serializer = TypeSerializer()
        xprv = {k: serializer.serialize(v) for k,v in xprv.items()}
        response = self.client.query(
            TableName=self.table_name,
            KeyConditionExpression=condition_expr,
            ExpressionAttributeValues=xprv,
            ExpressionAttributeNames=xprn
        )
        deserializer = TypeDeserializer()
        if response["Items"]:
            items = []
            for item in response["Items"]:
                item = {k: deserializer.deserialize(v) for k, v in item.items()}
                items.append(item)
            return items
        return None

class UploadsJournal(Journal):
    def save(self, u_file):
        my_date = datetime.now()
        my_iso_date = my_date.isoformat()
        data = {
            "uid": u_file.uid,
            "file_name": u_file.file_name,
            "file_path": u_file.file_path,
            "created_at": my_iso_date,
            "status": "CREATED"
        }
        # save to upload files list
        self.put_record("files", my_iso_date, data)

        # save file metadata
        self.put_record(f"files:{u_file.uid}", "meta", data)

        # save file parts
        counter = 1
        for part in u_file.chunks:
            self.put_record(f"files:{u_file.uid}", f"parts:{counter}", part)
            counter = counter + 1
    
    def update_meta(self, u_file, key, value):
        self.update_record(f"files:{u_file.uid}", "meta", key, value)

    def update_part(self, u_file, part_num, key, value):
         self.update_record(f"files:{u_file.uid}", f"parts:{part_num}", key, value)

import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(profile_name=os.getenv("AWS_PROFILE",''))
client = session.client('s3')

class UploadManager:
    def __init__(self, bucket="examplebucket", prefix=""):
        self.client = client
        self.bucket = bucket
        self.prefix = prefix

    def gen_file_key(self, name):
        return "/".join([x for x in [self.prefix, name] if x])
    
    # Initiate the upload
    def init_upload(self, name="largeobject"):
        key = self.gen_file_key(name)
        response = self.client.create_multipart_upload(
            Bucket=self.bucket,
            # ContentType='application/zip',
            Key=key,
        )
        """ Expected Output:
        {
            'Bucket': 'examplebucket',
            'Key': 'largeobject',
            'UploadId': 'ibZBv_75gd9r8lH_gqXatLdxMVpAlj6ZQjEs.OwyF3953YdwbcQnMA2BLGn8Lx12fQNICtMw5KyteFeHw.Sjng--',
            'ResponseMetadata': {
                '...': '...',
            },
        }
        """

        # Todo: log the response for debugging

        return { "succeeded": True, "bucket": response["Bucket"], "key": response["Key"], "upload_id": response["UploadId"] }

    def upload_part(self, body, name, part_num, upload_id):
        key = self.gen_file_key(name)
        print('counter', part_num, 'key', key)
        response = self.client.upload_part(
                Body=body,
                Bucket=self.bucket,
                Key=key,
                PartNumber=part_num,
                UploadId=upload_id,
            )
        """ Expected Output:
        {
            'ETag': '"d8c2eafd90c266e19ab9dcacc479f8af"',
            'ResponseMetadata': {
                '...': '...',
            },
        }
        """
        return response

    def upload_files(self, name, files, upload_id):
        parts = []
        # Upload each part
        counter = 0
        for fi in files:
            counter = counter + 1
            part_num = str(counter)
            with open(fi["path"], 'rb') as f:
                file_body = f.read()
                response = self.upload_part(file_body, name, counter, upload_id)
                parts.append({
                    "counter": counter,
                    "part_num": part_num,
                    "etag": response["ETag"],
                    "name": name,
                })

        return { "succeeded": True, "parts": parts, "parts_count": counter }

    def list_uploaded_files(self):
        # List uploaded parts 
        response = self.client.list_multipart_uploads(
            Bucket=self.bucket,
            # Delimiter='string',
            # EncodingType='url',
            # KeyMarker='string',
            # MaxUploads=123,
            Prefix=self.prefix,
            # UploadIdMarker='string',
        )
        """ Expected Output:

        {
            'Uploads': [
                {
                    'Initiated': datetime(2014, 5, 1, 5, 40, 58, 3, 121, 0),
                    'Initiator': {
                        'DisplayName': 'display-name',
                        'ID': 'examplee7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'Key': 'JavaFile',
                    'Owner': {
                        'DisplayName': 'display-name',
                        'ID': 'examplee7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'StorageClass': 'STANDARD',
                    'UploadId': 'examplelUa.CInXklLQtSMJITdUnoZ1Y5GACB5UckOtspm5zbDMCkPF_qkfZzMiFZ6dksmcnqxJyIBvQMG9X9Q--',
                },
                {
                    'Initiated': datetime(2014, 5, 1, 5, 41, 27, 3, 121, 0),
                    'Initiator': {
                        'DisplayName': 'display-name',
                        'ID': 'examplee7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'Key': 'JavaFile',
                    'Owner': {
                        'DisplayName': 'display-name',
                        'ID': 'examplee7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'StorageClass': 'STANDARD',
                    'UploadId': 'examplelo91lv1iwvWpvCiJWugw2xXLPAD7Z8cJyX9.WiIRgNrdG6Ldsn.9FtS63TCl1Uf5faTB.1U5Ckcbmdw--',
                },
            ],
            'ResponseMetadata': {
                '...': '...',
            },
        }
        """

        return response

    def list_uploaded_files_by_marker(self):
        # List uploaded parts using a marker
        response = self.client.list_multipart_uploads(
            Bucket=self.bucket,
            KeyMarker='nextkeyfrompreviousresponse',
            MaxUploads='2',
            UploadIdMarker='valuefrompreviousresponse',
        )

        """ Expected Output:

        {
            'Bucket': 'acl1',
            'IsTruncated': True,
            'KeyMarker': '',
            'MaxUploads': '2',
            'NextKeyMarker': 'someobjectkey',
            'NextUploadIdMarker': 'examplelo91lv1iwvWpvCiJWugw2xXLPAD7Z8cJyX9.WiIRgNrdG6Ldsn.9FtS63TCl1Uf5faTB.1U5Ckcbmdw--',
            'UploadIdMarker': '',
            'Uploads': [
                {
                    'Initiated': datetime(2014, 5, 1, 5, 40, 58, 3, 121, 0),
                    'Initiator': {
                        'DisplayName': 'ownder-display-name',
                        'ID': 'examplee7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'Key': 'JavaFile',
                    'Owner': {
                        'DisplayName': 'mohanataws',
                        'ID': '852b113e7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'StorageClass': 'STANDARD',
                    'UploadId': 'gZ30jIqlUa.CInXklLQtSMJITdUnoZ1Y5GACB5UckOtspm5zbDMCkPF_qkfZzMiFZ6dksmcnqxJyIBvQMG9X9Q--',
                },
                {
                    'Initiated': datetime(2014, 5, 1, 5, 41, 27, 3, 121, 0),
                    'Initiator': {
                        'DisplayName': 'ownder-display-name',
                        'ID': 'examplee7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'Key': 'JavaFile',
                    'Owner': {
                        'DisplayName': 'ownder-display-name',
                        'ID': 'examplee7a2f25102679df27bb0ae12b3f85be6f290b936c4393484be31bebcc',
                    },
                    'StorageClass': 'STANDARD',
                    'UploadId': 'b7tZSqIlo91lv1iwvWpvCiJWugw2xXLPAD7Z8cJyX9.WiIRgNrdG6Ldsn.9FtS63TCl1Uf5faTB.1U5Ckcbmdw--',
                },
            ],
            'ResponseMetadata': {
                '...': '...',
            },
        }
        """

    def complete_upload(self, name, parts, upload_id):
        key = self.gen_file_key(name)
        # Complete the multipart upload
        print('key', key)
        response = self.client.complete_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            MultipartUpload={
                'Parts': [ {"ETag": part["etag"], "PartNumber": part["part_num"] } for part in parts],
            },
            UploadId=upload_id
        )
        """ Expected Output:
        {
            'Bucket': 'acexamplebucket',
            'ETag': '"4d9031c7644d8081c2829f4ea23c55f7-2"',
            'Key': 'bigobject',
            'Location': 'https://examplebucket.s3.amazonaws.com/bigobject',
            'ResponseMetadata': {
                '...': '...',
            },
        }
        """
        return response

    def cancel_upload(self, name, upload_id):
        key = self.gen_file_key(name)
        response = self.client.abort_multipart_upload(
            Bucket=self.bucket,
            Key=key,
            UploadId=upload_id
        )
        """ Expected Output:
        {
            'ResponseMetadata': {
                '...': '...',
            },
        }
        """
        return response
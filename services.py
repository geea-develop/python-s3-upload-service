import os
import boto3
from options import OPTION, load_options

from file_manager import FileManager
from journal import UploadsJournal
from upload_manager import UploadManager

options = load_options()

file_manager = FileManager()

session = boto3.Session(profile_name=os.getenv("AWS_PROFILE",''))
client = session.client('s3')
upload_manager = UploadManager(client, bucket=os.getenv("S3_BUCKET", "my-s3-bucket"), prefix=os.getenv("S3_PREFIX", "my-folder"))

session = boto3.Session(profile_name="default")
client = session.client('dynamodb', endpoint_url=options.get(OPTION.dynamodb_endpoint), region_name=options.get(OPTION.dynamodb_region))
journal = UploadsJournal(client, options.get(OPTION.dynamodb_table))
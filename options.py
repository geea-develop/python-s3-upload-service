import argparse
import csv
import enum
import os
from xmlrpc.client import boolean
from dotenv import load_dotenv

# map arguments to easy to use python enum
class OPTION(enum.Enum):
    file_path = "fpath"
    dynamodb_table = "dynamodbtable"
    dynamodb_endpoint = "dynamodbendpoint"
    dynamodb_region = "dynamodbregion"
    aws_profile = "awsprofile"
    aws_region = "awsregion"
    s3_bucket = "s3bucket"
    s3_prefix = "s3prefix"
    s3_region = "s3region"

class Options:
    def get(self, name: OPTION):
        if self.has(name):
            return getattr(self, name.value)
    def has(self, name: OPTION) -> boolean:
        return isinstance(name, OPTION)


# Load env variables
load_dotenv()

# create options class
options = Options()
parser = argparse.ArgumentParser()

# File (to be uploaded) options
parser.add_argument(f"--{OPTION.file_path.value}", help='File path to be uploaded', type=str)

# Dynamodb options
parser.add_argument(f"--{OPTION.dynamodb_table.value}", help='DYNAMODB_TABLE default Uploads', default=os.getenv("DYNAMODB_TABLE", "Uploads"), type=str)
parser.add_argument(f"--{OPTION.dynamodb_endpoint.value}", help='DYNAMODB_ENDPOINT default http://localhost:8000', default=os.getenv("DYNAMODB_ENDPOINT", ""), type=str)
parser.add_argument(f"--{OPTION.dynamodb_region.value}", help='DYNAMODB_REGION default AWS_REGION', default=os.getenv("DYNAMODB_REGION", os.getenv('AWS_REGION')), type=str)

# aws options
parser.add_argument(f"--{OPTION.aws_profile.value}", help='AWS_PROFILE default ', default=os.getenv('AWS_PROFILE'), type=str)
parser.add_argument(f"--{OPTION.aws_region.value}", help='AWS_REGION default AWS_REGION', default='eu-west-1', type=str)

# s3 options
parser.add_argument(f"--{OPTION.s3_bucket.value}", help='S3_BUCKET default my-s3-bucket', default=os.getenv('S3_BUCKET'), type=str)
parser.add_argument(f"--{OPTION.s3_prefix.value}", help='S3_PREFIX default my-path', default=os.getenv('S3_PREFIX'), type=str)
parser.add_argument(f"--{OPTION.s3_region.value}", help='S3_REGION default AWS_REGION', default=os.getenv('AWS_REGION'), type=str)

args = parser.parse_args(namespace=options)

def load_options() -> Options:
    return options
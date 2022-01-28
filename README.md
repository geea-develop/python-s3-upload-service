# Python s3 upload service

## Create virtual env
`python3 -m venv venv`

## Enter virtual env
`source venv/bin/activate`

## Install dependencies
`pip install -r requirements.txt`

## upload file
`./upload_file.py --fpath ./samples/pictures.zip`

## Run the dynamodb locally
`docker run --rm -d -p 8000:8000 amazon/dynamodb-local`

## Working with dynamodb
### List tables
`aws dynamodb list-tables --endpoint-url http://localhost:8000 --region eu-west-1`

### Create Uploads table
```
aws dynamodb create-table \
    --table-name Uploads \
    --attribute-definitions \
        AttributeName=PPK,AttributeType=S \
        AttributeName=PRK,AttributeType=S \
    --key-schema \
        AttributeName=PPK,KeyType=HASH \
        AttributeName=PRK,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=10,WriteCapacityUnits=5 \
    --endpoint-url http://localhost:8000 \
    --region eu-west-1
```

### OLD Key Types:
 - PPK = "files", PRK = {datetime}
 - PPK = "file":{uid}, PRK = "metadata"
 - PPK = "file":{uid}, PRK = "chunks":{counter}
 - PPK = "file":{uid}:"chunk":{counter}, PRK = "metadata"
 - PPK = "file":{uid}:"chunk":{counter}:"attempts", PRK = {datetime}

### NEW Key Types:
 - PPK = "files", PRK = {datetime}
 - PPK = "files":{uid}, PRK = "meta"
 - PPK = "files":{uid}, PRK = "parts":{counter}
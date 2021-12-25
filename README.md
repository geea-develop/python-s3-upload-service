# Python s3 upload service

## Create virtual env
`python -m venv venv`

## Enter virtual env
`source venv/bin/activate`

## Install dependencies
`pip install -r requirements.txt`

## split file into chunks
`python main.py --file ./samples/pictures.zip`

## merge chunks into a file
`python main.py --action merge --chunks ./out`

## upload file
`python main.py --action upload --file ./samples/pictures.zip`

## using aws profile
`python main.py --file ./samples/pictures.zip`

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

### Key Types:
 - PPK = "files", PRK = {datetime}
 - PPK = "file":{uid}, PRK = "metadata"
 - PPK = "file":{uid}, PRK = "chunks":{counter}
 - PPK = "file":{uid}:"chunk":{counter}, PRK = "metadata"
 - PPK = "file":{uid}:"chunk":{counter}:"attempts", PRK = {datetime}

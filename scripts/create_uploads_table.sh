#!/bin/sh

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

echo "Created uploads table."
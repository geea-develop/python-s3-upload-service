#!/bin/sh

docker run --rm -d -p 8000:8000 amazon/dynamodb-local

echo "Running dynamodb db locally."
echo "Connection endpoint: http://localhost:8000"
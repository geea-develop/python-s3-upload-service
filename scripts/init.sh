#!/bin/sh

python3 -m venv venv

echo "Created virtual environment."

source venv/bin/activate

echo "Attached environment."

pip install -r requirements.txt

echo "Installed dependencies."
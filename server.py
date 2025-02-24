import threading
import boto3
from flask import Flask, request
import os
from dotenv import load_dotenv

# Loading Environment Variables
load_dotenv()
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
region_name = os.getenv('region_name')

# AWS S3 Client Initialization
s3_client = boto3.client('s3', 
                    aws_access_key_id=aws_access_key_id, 
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name)

# AWS SDB client Initialization
sdb_client = boto3.client('sdb', 
                            aws_access_key_id=aws_access_key_id, 
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

# Function to upload file to S3
def uploadFileObj(file_data, bucket_name, s3_file_key):
    s3_client.put_object(Body=file_data, 
                        Bucket=bucket_name, 
                        Key=s3_file_key)
    
# Function to get image class from SDB
def get_image_class(image_file_name: str):
    res = sdb_client.get_attributes(DomainName='1229855265-simpleDB',
                            ItemName=image_file_name)
    
    return res



# Flask app initialization
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def home():
    
    # Home route GET request for testing
    if request.method == 'GET':
        return "Hello"
    
    # The POST request 
    if request.method == 'POST':
        inputFile = request.files['inputFile'] 
        bucket_name = '1229855265-in-bucket'
        s3_file_key = inputFile.filename 
        
        file_data = inputFile.read()
        
        # Starting a deifferent thread for file upload to S3
        s3_upload_thread = threading.Thread(
            target=uploadFileObj,
            args=(file_data, bucket_name, s3_file_key)
        )
        s3_upload_thread.start()
        
        # Retrieving image class
        res = get_image_class(s3_file_key.split('.')[0])
        
        final_output = f"{s3_file_key}:{res['Attributes'][0]['Value']}"

        return final_output
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)





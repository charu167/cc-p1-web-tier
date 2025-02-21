import threading
from io import BytesIO
import boto3
from flask import Flask, request
import os
from dotenv import load_dotenv




load_dotenv()
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
region_name = os.getenv('region_name')
s3 = boto3.client('s3', 
                    aws_access_key_id=aws_access_key_id, 
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name)

sdb_client = boto3.client('sdb', 
                            aws_access_key_id=aws_access_key_id, 
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

def uploadFileObj(file_data, bucket_name, s3_file_key):
    res = s3.put_object(Body=file_data, 
                        Bucket=bucket_name, 
                        Key=s3_file_key)
    print(f"res: ${res}\nSuccessfully uploaded the file to S3")
    
def get_image_class(image_file_name: str):
    res = sdb_client.get_attributes(DomainName='1229855265-simpleDB',
                            ItemName=image_file_name)
    
    return res




app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'GET':
        return "Hello"
    
    
    if request.method == 'POST':
        inputFile = request.files['inputFile']  # Access the file using the field name
        bucket_name = '1229855265-in-bucket'
        s3_file_key = inputFile.filename  # Use the filename as the S3 key
        
        file_data = inputFile.read()
        # uploadFileObj(inputFile, bucket_name, s3_file_key)
        s3_upload_thread = threading.Thread(
            target=uploadFileObj,
            args=(file_data, bucket_name, s3_file_key)
        )
        s3_upload_thread.start()
        
        res = get_image_class(s3_file_key.split('.')[0])
        
        s = f"{s3_file_key}:{res['Attributes'][0]['Value']}"

        return s
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)





import boto3
from flask import Flask, request
import os
from dotenv import load_dotenv



load_dotenv()
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
region_name = os.getenv('region_name')


def uploadFileObj(file_obj, bucket_name, s3_file_key):
    s3 = boto3.client('s3', 
                    aws_access_key_id=aws_access_key_id, 
                    aws_secret_access_key=aws_secret_access_key,
                    region_name=region_name)
    
    s3.upload_fileobj(file_obj, bucket_name, s3_file_key)
    
def get_image_class(image_file_name: str):
    sdb_client = boto3.client('sdb', 
                            aws_access_key_id=aws_access_key_id, 
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)

    res = sdb_client.get_attributes(DomainName='1229855265-simpleDB',
                            ItemName=image_file_name)
    
    return res




app = Flask(__name__)

@app.route("/", methods=['POST'])
def home():
    if request.method == 'POST':
        inputFile = request.files['inputFile']  # Access the file using the field name
        bucket_name = '1229855265-in-bucket'
        s3_file_key = inputFile.filename  # Use the filename as the S3 key
       
        uploadFileObj(inputFile, bucket_name, s3_file_key)
        res = get_image_class(s3_file_key.split('.')[0])
        
        s = f"{s3_file_key}:{res['Attributes'][0]['Value']}"

        return s

if __name__ == "__main__":
    app.run(debug=True, port=8000)





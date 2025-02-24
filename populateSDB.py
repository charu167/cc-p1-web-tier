import pandas as pd
import os
from dotenv import load_dotenv
import boto3

load_dotenv()
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
region_name = os.getenv('region_name')

sdb_client = boto3.client('sdb', 
                        aws_access_key_id=aws_access_key_id, 
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)

def createDomain(domain_name: str):
    try:
        domain_created = sdb_client.create_domain(DomainName=domain_name)
        return domain_created
    except Exception as e:
        print(e)

def deleteDomain(domain_name: str):
    try:
        domain_deleted = sdb_client.delete_domain(DomainName=domain_name)
        return domain_deleted
    except Exception as e:
        print(e)

class Image:
    def __init__(self, file_name, person_name) -> None:
        self.file_name = file_name
        self.person_name = person_name
        
    def pushToSDB(self):
        try:
            res = sdb_client.put_attributes(DomainName='1229855265-simpleDB',
                            ItemName=self.file_name,
                            Attributes=[{ 'Name': 'person_name', 'Value': self.person_name}]
                            )
            print(res)
            return res
        except Exception as e:
            print(f"Error pushing to SimpleDB: {e}")
            return None
        
    
    

if __name__ == '__main__':
    # deleteDomain(domain_name='1229855265-simpleDB')
    createDomain(domain_name='1229855265-simpleDB')
    try:
        csv_file_path = '/Users/charudattapotdar/Desktop/CC/Project1/web-tier/Classification Results on Face Dataset (1000 images).csv'
        dataframe = pd.read_csv(csv_file_path)

        for idx, item in dataframe.iterrows():
            image = Image(file_name=item['Image'], person_name=item['Results'])
            result = image.pushToSDB()
            if result:
                print(f"Successfully pushed {item['Image']} to SimpleDB")
    except Exception as e:
        print(f"Error while processing the images CSV: {e}")
        
    
        

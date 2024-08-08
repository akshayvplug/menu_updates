
# Script to fetch chain ID & names for a rest.
# Initialize the menu class and pass the store id's.
import hashlib
import json
import os
import csv
from pathlib import Path
from typing import Text
from zipfile import ZipFile

import boto3
import botocore
import xmltodict

# VP_ENVIRONMENT = os.environ.get('VP_ENVIRONMENT')
VP_ENVIRONMENT = 'production'
S3_BUCKET_NAME = 'pos-menu-data'
AWS_REGION_NAME = 'us-east-1'

if not VP_ENVIRONMENT:
    # Terminate Program if not set.
    raise ValueError('Environment Variable "VP_ENVIRONMENT" is not set')


class Menu():

    """
    Loads the menu for the given restaurant from the local copy.
    If the local copy is outdated, downloads a updated copy from 
    AWS S3.

    USAGE: 
    Initialize a Menu object by passing the rest_abbr, vendor ID.
    >> cap_menu = Menu('mmr', 6157)
    
    Call the "load_menu()" method which will return the menu as a dict.
    >> cap_menu.load_menu()
    """

    def __init__(self, rest_abbr: Text, vendorid: int) -> None:
        self.rest_abbr = rest_abbr
        self.vendorid = vendorid
        self.file_name = f"{rest_abbr.upper()}-{vendorid}.zip"
        self.key_name = f"{VP_ENVIRONMENT}/olo/{self.file_name}"

        self.load_menu()
        self.get_product_names()


    @classmethod
    def get_client(cls):
        """ Creates a S3 client object """
        s3 = boto3.client(
            service_name = 's3',
            aws_access_key_id = os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key = os.environ['AWS_SECRET_KEY'],
            region_name = AWS_REGION_NAME,
            )

        return s3


    def has_local_copy(self):
        """ Checks if a local copy of menu zip exists in current folder """

        print(f"**** Checking from local copy method **** ")
        print(f"File Name : menu_files/{self.file_name}")
        print(f"Current Dir : {os.path.curdir}")

        # if os.path.exists(path = f"menu_files/{self.file_name}"):
        #     return True
        
        return os.path.exists(
                    path = f"menu_files/{self.file_name}"
                    )


    def get_md5_local_copy(self) -> Text:
        """ Generates md5 hash for the local copy """

        md5_hash = hashlib.md5()

        with open(f"menu_files/{self.file_name}", 'rb') as content:
            md5_hash.update(content.read())
        
        return md5_hash.hexdigest()


    def get_md5_aws_copy(self,) -> Text:
        """ Gets md5 hash for the copy available in AWS """

        s3 = Menu.get_client()
        digest = None

        try:
            files = s3.list_objects(Bucket = S3_BUCKET_NAME)
        except botocore.exceptions.ClientError as e:
            print(f"Encountered exception : {e.response['Error']['Code']}")
            print(f"Exception Message : {e.response['Error']['Message']}")
            pass      

        for file in files['Contents']:
            if file['Key'] == self.key_name:
                digest = file['ETag'].strip('"')
                break

        return digest


    def download_from_s3(self,):
        """ Downloads a copy of menu zip from AWS S3 & save in local dir """

        s3 = Menu.get_client()

        # creates a dir to store all menu files.
        menu_dir = 'menu_files'
        if not os.path.exists(path= menu_dir):
            os.mkdir(path= menu_dir)

        try:
            with open(f"menu_files/{self.file_name}", 'wb') as data:
                s3.download_fileobj(S3_BUCKET_NAME, self.key_name, data)
        except botocore.exceptions.ClientError as e:
            print(f"Encountered exception : {e.response['Error']['Code']}")
            print(f"Exception Message : {e.response['Error']['Message']}")
            pass
        
        return None

    
    def load_menu(self,):
        """ Extract the zip file, parse the xml & load as dict """

        if not self.has_local_copy():
            print(f"File not available locally. Downloading from AWS...")
            self.download_from_s3()
        elif self.get_md5_local_copy() != self.get_md5_aws_copy():
            print(f"MD5 Hash is different. Downloading from AWS...")
            print(f"Local Hash : {self.get_md5_local_copy()}")
            print(f"AWS Hash : {self.get_md5_aws_copy()}")

            self.download_from_s3()
        else:
            print(f"Using local copy....")
        
        print(f"./menu_files/{self.file_name}")
        with ZipFile(f"menu_files/{self.file_name}", 'r') as zip_f:
            with zip_f.open(f"{self.vendorid}.xml") as xml_input:
                olo = xmltodict.parse(
                                xml_input= xml_input, 
                                encoding= "UTF-8", 
                                )
                olo = json.dumps(olo)
                olo = json.loads(olo)

                # print(olo)
        
        self.menu = olo['restaurant']['menu']

        return self.menu

    
    def get_product_names(self,):
        """ 
        Unpack each product from its category 
        and returns a list of product names & product info
        """
        
        self.products = []
        self.product_names = []

        for category in self.menu['categories']['category']:
            for prod in category['products']['product']:

                # Category containing only 1 product is represented
                # directly as a dict rather than usual list of dict.
                if isinstance(prod, list):
                    for p in prod:
                        self.product_names.append(p['@name'])
                        self.products.append(p)

                elif isinstance(prod, dict):
                    self.product_names.append(prod['@name'])
                    self.products.append(prod)
        
        # print(f"Product Name : \n {self.product_names}")

        return None





prod_array = []

OLK_STORES = [6155, 6157, 6144, 6158, 6133, 6140, 30377, 6166, 34285, 6135, 66312, 6162, 6168, 6169, 6146, 6153]

OAK_STORES = [6152, 6167, 6149]


store_ids = OLK_STORES
rest_abbr = 'OLK'

item_info = {}

for id in store_ids:
    print(f"Processing for {id}")
    menu = Menu(rest_abbr, id)
    products = menu.products

    for p in products:
        

        if not item_info.get(p.get('@name')):
            item_info[p.get('@name')] = {}

        # if not item_info.get('availability'):
        #     item_info['availability'] = {}

        if not item_info[p.get('@name')].get(id):
            item_info[p.get('@name')][id] = {}

        # item_info[p.get('@name')][id]['isavailable'] = True
        item_info[p.get('@name')][id]['posproductid'] = str(p.get('@id'))
        # item_info[p.get('@name')][id]['chainproductid'] = str(p.get('@chainproductid'))

print(item_info)



with open(f"{rest_abbr}_availability_data.csv", 'w', newline= '') as csvfile:
    csvwriter = csv.DictWriter(
                    csvfile,
                    fieldnames= ['pos_name', 'data']
    )

    for k, v in item_info.items():
        csvwriter.writerow(
            {
                'pos_name' : k,
                'data' : f"'{json.dumps(v)}'"
            }
        )

    print(f"Successfully completed...")

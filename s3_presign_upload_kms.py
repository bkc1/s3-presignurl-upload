
import boto3
import argparse
import datetime
from botocore.client import Config
from requests import Request, Session

parser = argparse.ArgumentParser(description='Generate S3 Presigned URL and upload file using SSE-KMS encyption')
parser.add_argument('-r','--region', help='AWS region', required=True)
parser.add_argument('-b','--bucket', help='S3 bucket name', required=True)
parser.add_argument('-o','--object_key', help='S3 object key', required=True)
parser.add_argument('-k','--kms_key', help='KMS key ID', required=True)
parser.add_argument('-f','--filepath', help='local file path', required=True)
parser.add_argument('-d','--debug', help='enable debugging', action='store_true')

args = parser.parse_args()

REGION = (args.region)
YOUR_BUCKET = (args.bucket)
KEY_NAME = (args.object_key)
KMS_KEY_ID = (args.kms_key)
PATH_TO_LOCAL_FILE = (args.filepath)

# Create S3 client object
s3 = boto3.client('s3', config=Config(signature_version='s3v4', region_name=REGION))

# Set object expiry time to be 604800 seconds after current time. Format must be in compliance with RFC 1123. (e.g. Thu, 01 Dec 1994 16:00:00 GMT)
expires = (datetime.datetime.now() + datetime.timedelta(0,604800)).strftime("%a, %d %b %Y %H:%M:%S GMT")

# Define ClientMethod paramters for pre-signed URL
params = {
  'Bucket': YOUR_BUCKET,
  'Key': KEY_NAME,
  'Expires': expires,
  'ServerSideEncryption': 'aws:kms',
  'SSEKMSKeyId': KMS_KEY_ID,
  'ACL': 'public-read'
}

# Generate the pre-signed URL
url = s3.generate_presigned_url(
  ClientMethod='put_object',
  Params=params
)

# DEBUG: Print the presigned URL if -d is set
if args.debug: 
  print ('This is the presigned URL: ' + str(url) )

# Read the local file to pass as the body in the HTTP request
with open(PATH_TO_LOCAL_FILE, 'rb') as readFile:
  payload = readFile.read()

#=================================#
#      MAKE THE HTTP REQUEST      #
#=================================#

# Define HTTP Request headers
headers = {
  "Expires": str(expires),
  "x-amz-acl": "public-read",
  "x-amz-server-side-encryption": "aws:kms",
  "x-amz-server-side-encryption-aws-kms-key-id": KMS_KEY_ID
}

# New Session object for HTTP Request
s = Session()

# Compile HTTP request
request = Request('PUT', url, data=payload, headers=headers)
prep = request.prepare()

# Perform HTTP request
response = s.send(prep)

# Print out the HTTP response from S3
print(response.text)


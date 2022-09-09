import boto3
from ec2_metadata import ec2_metadata


# Get role and account ID from EC2 metadata
role_name = ec2_metadata.instance_profile_name
acct_id = ec2_metadata.account_id
region = ec2_metadata.region

# Assume role & get credentials
sts_client = boto3.client('sts')
response = sts_client.assume_role(
    RoleArn=(f'arn:aws:iam::{acct_id}:role/{role_name}'),
    RoleSessionName=role_name
)

# Instantiate a session based on them
session = boto3.Session(
    aws_access_key_id=response['Credentials']['AccessKeyId'],
    aws_secret_access_key=response['Credentials']['SecretAccessKey'],
    aws_session_token=response['Credentials']['SessionToken'],
    region_name=region
)

s3_client = boto3.client('s3')


# TODO update bucket,key and expiration time
params = {
  'Bucket': '<mybucket>',
  'Key': '<myfile.png>',
  'ResponseExpires': 3600
}


url = s3_client.generate_presigned_url('get_object', Params=params,)
print(url)

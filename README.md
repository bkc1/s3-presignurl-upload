## Upload files to S3 with SSE-KMS encyption using Pre-Signed URLs

This Python3 script uses the Boto3 AWS SDK to upload files to S3 using SSE-KMS encrpytion with pre-signed URLs.

### Usage

```
$ python3 s3_presign_upload_kms.py --help
usage: s3_presign_upload_kms.py [-h] -r REGION -b BUCKET -o OBJECT_KEY -k
                                KMS_KEY -f FILEPATH [-d]

Generate S3 Presigned URL and upload file using SSE-KMS encyption

optional arguments:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        AWS region
  -b BUCKET, --bucket BUCKET
                        S3 bucket name
  -o OBJECT_KEY, --object_key OBJECT_KEY
                        S3 object key
  -k KMS_KEY, --kms_key KMS_KEY
                        KMS key ID
  -f FILEPATH, --filepath FILEPATH
                        local file path
  -d, --debug           enable debugging
```
Example with the debug option specified:
```
$ python3 s3_presign_upload_kms.py -d  -r us-east-1 -b mybucket -o my_object -k f85f8f32-8e65-40bd-a6fe-XXXXXXXXX -f path/to/my/local/file
```
Preferred method using pipenv:
```
$ pipenv install
$ pipenv run "python s3_presign_upload_kms.py -d  -r us-east-1 -b mybucket -o my_object -k f85f8f32-8e65-40bd-a6fe-XXXXXXXXX -f path/to/my/local/file"
```


import boto3
from werkzeug.security import generate_password_hash
from datetime import datetime as dt


def upload_file_to_s3(file_path, bucket_name=None, key_name=None, region_name=None):
    s3 = boto3.resource('s3', region_name=region_name)
    bucket = s3.Bucket(bucket_name)

    try:
        bucket.upload_file(Filename=file_path, Key=key_name)
        print("File uploaded successfully")
    except Exception as e:
        print(e)


# upload_file_to_s3(
#     file_path='instance/food-drive.db',
#     bucket_name='food-drive-database-bucket-benj-us-west-1',
#     key_name='food-drive.db',
#     region_name='us-west-1'
# )

print(generate_password_hash("Percival3512"))
print(dt.now())

import boto3


def upload_file_to_s3(file_path, bucket_name=None, key_name=None, region_name=None):
    s3 = boto3.resource('s3', region_name=region_name)
    bucket = s3.Bucket(bucket_name)

    try:
        bucket.upload_file(Filename=file_path, Key=key_name)
        print("File uploaded successfully")
    except Exception as e:
        print(e)

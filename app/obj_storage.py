import shared
import os
import boto3
from datetime import datetime

s3 = boto3.resource(**shared.s3_config)

#Upload photo to bucket and return the url
def upload_photo(image):
    try:
        #Get the file name
        bucket = "card-images"
        timestamp = datetime.utcnow().isoformat()
        filename = f"{timestamp}-{image.filename}"

        s3.Bucket(bucket).Object(filename).put(Body=image.read())

        print('Uploaded file to S3')

        return get_public_s3_url(filename)
    except Exception as e:
        return {"error": str(e)}

def get_public_s3_url(filename):
    return f"{os.environ.get('S3_ENDPOINT_URL')}{filename}"
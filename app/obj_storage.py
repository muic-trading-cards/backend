from app.shared import *
import os
import boto3
from datetime import datetime

s3 = boto3.resource(**s3_config)

#Upload photo to bucket and return the url
def upload_photo(image):
    try:
        #Get the file name
        bucket = "card-images"
        timestamp = datetime.utcnow().isoformat()
        #get the type of file that the image is
        filetype = image.filename.split('.')[-1]
        filename = f"{timestamp}{filetype}"

        s3.Bucket(bucket).Object(filename).put(Body=image.read(), ContentType='image/jpeg')

        print('Uploaded file to S3')

        return get_public_s3_url(filename)
    except Exception as e:
        return {"error": str(e)}


def get_public_s3_url(filename):
    return f"http://{s3_host}:{s3_port}/card-images/{filename}"
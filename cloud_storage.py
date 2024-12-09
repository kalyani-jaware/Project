from google.cloud import storage
from config import GOOGLE_CLOUD_BUCKET_NAME

def upload_to_gcs(file_path, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(GOOGLE_CLOUD_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    print(f"File {file_path} uploaded to {destination_blob_name}.")

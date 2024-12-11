from google.cloud import storage
from config import GOOGLE_CLOUD_BUCKET_NAME
import os

# print(os.cwd())
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/kaja7104_colorado_edu/service-credentials.json"

def upload_to_gcs(file_path, destination_blob_name):
    client = storage.Client(project='lab-5-437901')
    bucket = client.bucket(GOOGLE_CLOUD_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    print(f"File {file_path} uploaded to {destination_blob_name}.")

# Print out the Google Application Credentials path to confirm it's set
print("GOOGLE_APPLICATION_CREDENTIALS:", os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

# Create a Google Cloud Storage client
client = storage.Client()

# Output the project ID associated with the credentials
print("Project ID:", client.project)


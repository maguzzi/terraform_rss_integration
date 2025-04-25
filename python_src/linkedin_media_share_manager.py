import tempfile
import urllib.request
import os
import shutil
import requests

from logger import logger

headers = {
    "Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}",
    "Content-Type": "image/webp",
}

def preare_media_for_post(processed_post,profile_id):
  upload_url_urn = get_upload_url_urn(profile_id)
  filepath = download_image(processed_post["image"])
  upload_image(upload_url_urn["upload_url"],filepath)
  return upload_url_urn["asset_urn"]


def download_image(image_url):
  temp_dir = tempfile.mkdtemp()
  filepath = os.path.join(temp_dir, image_url.split("/")[-1])
  with urllib.request.urlopen(image_url) as response, open(filepath, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
  print(filepath)  
  return filepath

def upload_image(url,file_path):
  with open(file_path, 'rb') as file:
    file_content = file.read()
  response = requests.post(url, data=file_content, headers=headers)

def call_linkedin_get_upload_url(json_payload):
  url = "https://api.linkedin.com/v2/assets?action=registerUpload"
  response = requests.post(url, headers=headers, json=json_payload)
  logger.info(f"response to {url} => {response}")
  return response

def get_upload_url_urn(profile_id):

  json_payload = {
    "registerUploadRequest": {
      "recipes": [
        "urn:li:digitalmediaRecipe:feedshare-image"
      ],
      "owner": f"urn:li:person:{profile_id}", 
        "serviceRelationships": [
            {
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }
        ]
    }
  }

  register_upload_url_response = call_linkedin_get_upload_url(json_payload)

  logger.info(f"{register_upload_url_response}")

  response_json = register_upload_url_response.json()
  
  upload_url = response_json["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
  asset_urn = response_json["value"]["asset"]

  return {
    "upload_url": upload_url,
    "asset_urn": asset_urn
  }
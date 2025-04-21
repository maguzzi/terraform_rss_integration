import tempfile
import urllib.request
import os
import shutil
import requests

headers = {
    "Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}",
    "Content-Type": "image/webp",
}

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

def get_upload_url(profile_id):

  register_upload_url = "https://api.linkedin.com/v2/assets?action=registerUpload"

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

  response_json = requests.post(register_upload_url, headers=headers, json=json_payload).json()
  
  upload_url = response_json["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
  asset_urn = response_json["value"]["asset"]

  return {
    "upload_url": upload_url,
    "asset_urn": asset_urn
  }
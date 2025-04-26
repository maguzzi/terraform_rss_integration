import tempfile
import urllib.request
import os
import shutil
import requests
import requests_facade

from logger import logger

def preare_media_for_post(processed_post,profile_id):
  upload_url_urn = requests_facade.get_upload_url_urn(profile_id)
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
  requests_facade.upload_image(url,file_content)
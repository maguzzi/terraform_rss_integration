import requests
from logger import logger
import os

headers = {
    "Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}",
    "Content-Type": "image/webp",
}

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
  response =  post("https://api.linkedin.com/v2/assets?action=registerUpload",json_payload,200)
  
  response_json = response.json()
  
  upload_url = response_json["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
  asset_urn = response_json["value"]["asset"]

  return {
    "upload_url": upload_url,
    "asset_urn": asset_urn
  }  

def upload_image(url,data):
  put(url,data,201)

def publish_with_image_to_profile(profile_id,text,media_urn,title):
  json_payload = {
    "author": f"urn:li:person:{profile_id}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": f"{text}"
            },
            "shareMediaCategory": "IMAGE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": f"{title}"
                    },
                    "media":f"{media_urn}",
                    "title": {
                        "text": f"{title}"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }

  post("https://api.linkedin.com/v2/ugcPosts",json_payload,201)


def put(url,data,ok_code):
  response = requests.put(url, headers=headers, data=data)
  logger.info(f"response to {url} => {response}")
  check_response(response,ok_code)
  return response

def post(url,json_payload,ok_code):
  response = requests.post(url, headers=headers, json=json_payload)
  logger.info(f"response to {url} => {response}")
  check_response(response,ok_code)
  return response

def check_response(response,ok_code):
  if response.status_code == ok_code:
      logger.info("Request successful")
  else:
      logger.error(f"Request failed. Status code: {response.status_code} {response.text}")
      raise ValueError(response.text)
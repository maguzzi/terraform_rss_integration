import requests
from logger import logger
import os

headers = {
    "Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}",
    "LinkedIn-Version": "202504",
    "X-RestLi-Protocol-Version": "2.0.0"
}

def get_upload_url_urn(profile_id):
  
  json_payload = {
    "initializeUploadRequest": {
        "owner": f"urn:li:person:{profile_id}"
    }
  }
  
  response =  post("https://api.linkedin.com/rest/images?action=initializeUpload",json_payload,200)
  response_json = response.json()
  
  upload_url = response_json["value"]["uploadUrl"]
  asset_urn = response_json["value"]["image"]
  expires_at = response_json["value"]["uploadUrlExpiresAt"]

  logger.info(f"Upload successful for image {asset_urn}. Upload URL expires at {expires_at}")

  return {
    "upload_url": upload_url,
    "asset_urn": asset_urn
  }  

def upload_image(url,data):
  put(url,data,201)

def publish_to_profile(profile_id,text,media_urn,link,title,summary,mode):

  logger.info(f"link: {link}")
  logger.info(f"title: {title}")
  logger.info(f"summary: {summary}")
  logger.info(f"text: {text}")
  logger.info(f"media_urn: {media_urn}")

  content = None
  
  if mode == 'IMAGE' and media_urn is not None: # post contains image(s)
    content = {
        "media": {
            "id": media_urn,
            "altText": title
        }
    }
  elif mode == 'ARTICLE' and link is not None: # post contains link
    content = {
     "article": {
         "source": link,
         "title": title,
         "description": text,
         "thumbnail": media_urn
     }
    }

  json_payload = {
    "author": f"urn:li:person:{profile_id}",
    "commentary": text,
    "visibility": "PUBLIC",
    "distribution": {
        "feedDistribution": "MAIN_FEED",
        "targetEntities": [],
        "thirdPartyDistributionChannels": []
    },
    "lifecycleState": "PUBLISHED",
    "isReshareDisabledByAuthor": False,
    "content": content
  }

  post("https://api.linkedin.com/rest/posts",json_payload,201)


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
import requests
import os
import json
import linkedin_media_share_manager
from bs4 import BeautifulSoup
from logger import logger

import boto3

max_commentary_length=3000

headers = {
    "Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}",
    "Content-Type": "application/json",
  }

translate_client = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)

def translate(text):
    result = translate_client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode="it")
    tt = result.get('TranslatedText')
    logger.info('TranslatedText: ' + tt)

    return tt

def publish_to_profile(processed_post,profile_id):
  #asset_urn = linkedin_media_share_manager.preare_media_for_post(processed_post,profile_id)
  publish(processed_post,to_profile_payload(processed_post,profile_id,'asset_urn'))

def remove_html_tags_with_newlines(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')

    # Replace heading tags (h1 to h6) with newlines
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6','br','p']):
        tag.replace_with(tag.get_text() + '\n')

    for tag in soup.find_all(['li']):
        tag.replace_with(f"- {tag.get_text()}\n")

    return soup.get_text(separator='').strip()

def to_profile_payload(processed_post,profile_id,media_urn):
   
  text = remove_html_tags_with_newlines(processed_post.get("body","no body"))
  
  translated_text = translate(text)

  return {
    "author": f"urn:li:person:{profile_id}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": f"{translated_text} {processed_post.get("link","no link")}"[:max_commentary_length-1]
            },
            "shareMediaCategory": "IMAGE",
            "media": [
                {
                    "status": "READY",
                    "description": {
                        "text": f"{processed_post.get("title","no title")}"
                    },
                    "media":f"{media_urn}",
                    "title": {
                        "text": f"{processed_post.get("title","no title")}"
                    }
                }
            ]
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }


  

def publish(processed_post, json_payload):
  
  publish_url = "https://api.linkedin.com/v2/ugcPosts"
  
  logger.info(json_payload)

  #response = requests.post(publish_url, headers=headers, json=json_payload)

  #if response.status_code == 201:
  #    logger.info("Successfully posted to LinkedIn!")
  #    logger.debug(response.json())
  #else:
  #    logger.error(f"Failed to post to LinkedIn. Status code: {response.status_code}")
  #    logger.error(response.text)


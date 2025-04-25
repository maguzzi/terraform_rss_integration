import requests
import os
import json
import linkedin_media_share_manager

max_commentary_length=3000

headers = {
    "Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}",
    "Content-Type": "application/json",
  }

def publish_to_profile(processed_post,profile_id):
  asset_urn = linkedin_media_share_manager.preare_media_for_post(processed_post,profile_id)
  publish(processed_post,to_profile_payload(processed_post,profile_id,asset_urn))

       
def to_profile_payload(processed_post,profile_id,media_urn):

  return {
    "author": f"urn:li:person:{profile_id}",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": f"{processed_post.get("body","no body")} {processed_post.get("link","no link")}"[:max_commentary_length]
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
  
  response = requests.post(publish_url, headers=headers, json=json_payload)

  if response.status_code == 201:
      print("Successfully posted to LinkedIn!")
      print(response.json())
  else:
      print(f"Failed to post to LinkedIn. Status code: {response.status_code}")
      print(response.text)


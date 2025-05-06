import feedparser
import os
import social_publish_linkedin

import boto3
from boto3.dynamodb.conditions import Key

from logger import logger

dynamodb = boto3.resource('dynamodb')
dynamodb_table = os.environ.get("DYNAMODB_TABLE")
print(f"{dynamodb} - {dynamodb_table}")
table = dynamodb.Table(dynamodb_table)

def get_rss_url():
    return os.environ.get("RSS_URL")

def process_event(event, context):
    rss_url = get_rss_url()
    logger.info(f"reading from rss: {rss_url}")

    processed_post = process_latest_rss_post(rss_url)
    if (processed_post is not None):
        logger.info(processed_post)
        social_publish_linkedin.publish_to_profile(processed_post,os.environ.get("PROFILE_ID"),"ARTICLE")
        store_entry_in_dynamodb(rss_url,processed_post["latest_entry_id"])
        
    
def process_latest_rss_post(rss_url):

    try:
    
        latest_entry = if_not_written_return(rss_url)
        if (latest_entry is not None):
            result = {
                "title": latest_entry.get("title", "No Title"),
                "link": latest_entry.get("link", "No Link"),
                "summary": latest_entry.get("summary", "No Summary"),
                "body": None,
                "image": None,
                "latest_entry_id" : latest_entry.id
            }

            logger.info(result["summary"])

            if "content" in latest_entry:
                for item in latest_entry.content:
                    if item.type.startswith("image"):
                        result["image"] = item.get("src")
                    elif item.type == "text/html":
                        result["body"] = item.get("value")
                    else:
                        print("noop")

            logger.debug(result)
            return result
        else:
            return None    

        

    except Exception as e:
        print(f"Error processing RSS feed: {e}")
        return None

def if_not_written_return(rss_url,index=0):
  feed = feedparser.parse(rss_url)
  latest_entry = feed.entries[index]
  logger.info(f"query for {rss_url},{latest_entry.id}")
  response = table.query(
    KeyConditionExpression=Key('rss_id').eq(rss_url) & Key('post_id').eq(latest_entry.id)
  )
  logger.info(f"response {response}")
  if (response["Count"] == 0):
    return feed.entries[0]
  else:
    logger.info(f"entry with id {latest_entry.id} already present for rss {rss_url}")
  
def store_entry_in_dynamodb(rss_url,latest_entry_id):
  table.put_item(
    TableName=dynamodb_table,
    Item = {
        "rss_id": f"{rss_url}",
        "post_id": f"{latest_entry_id}"
        
    }
  )
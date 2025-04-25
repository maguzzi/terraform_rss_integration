import feedparser
import os
import social_publish_linkedin

from logger import logger

def process_event(event, context):
    rss_url = os.environ.get("RSS_URL")
    logger.info(f"reading from rss: {rss_url}")

    processed_post = process_latest_rss_post(rss_url)

    social_publish_linkedin.publish_to_profile(processed_post,os.environ.get("PROFILE_ID"))
    
def process_latest_rss_post(rss_url):

    try:
        feed = feedparser.parse(rss_url)

        # this is the most recent entry, to be improved
        latest_entry = feed.entries[0] 

        result = {
            "title": latest_entry.get("title", "No Title"),
            "link": latest_entry.get("link", "No Link"),
            "summary": latest_entry.get("summary", "No Summary"),
            "body": None,
            "image": None
        }

        if "content" in latest_entry:
            for item in latest_entry.content:
                if item.type.startswith("image"):
                    result["image"] = item.get("src")
                elif item.type == "text/html":
                    result["body"] = item.get("value")
                else:
                    print("noop")

        return result

    except Exception as e:
        print(f"Error processing RSS feed: {e}")
        return None

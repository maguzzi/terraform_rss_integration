import requests
import os
import json
import linkedin_media_share_manager
import requests_facade
from bs4 import BeautifulSoup
from logger import logger
from string import Template
import boto3
import re

## static definitions start ##

safeguard_message_length=2500

headers = {
    "Authorization": f"Bearer {os.environ.get("ACCESS_TOKEN")}",
    "Content-Type": "application/json",
  }

translate_client = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
template = Template(os.environ.get("MESSAGE_TEMPLATE"))

## static definitions end ##

def publish_to_profile(processed_post,profile_id):
  media_urn = linkedin_media_share_manager.prepare_media_for_post(processed_post,profile_id)
  text = prepare_text(processed_post)
  requests_facade.publish_to_profile(profile_id,text,media_urn,processed_post["link"],processed_post["title"],processed_post["summary"])
  
def prepare_text(processed_post):
  text_no_html = remove_html_tags_with_newlines(processed_post["summary"][:safeguard_message_length])
  data = {"translated_text":f"{escape_special_chars(translate(text_no_html))}"}
  return template.substitute(data)

def remove_html_tags_with_newlines(html_content):
  soup = BeautifulSoup(html_content, 'html.parser')

  for tag in soup.find_all(['br','p','ul','li','h1','h2','h3','h4','h5']):
    tag.replace_with(tag.get_text() + '\n')

  text = soup.get_text(separator='').strip()

  text = re.sub(r'\n{3,}', '\n\n', text)

  return text
    
def escape_special_chars(text):
    chars = ["\\", "|", "{", "}", "@", "[", "]", "(", ")", "<", ">", "#", "*", "_", "~"]
    backslash = '\\'
    for char in chars:
        text = text.replace(char, backslash+char)
    return text

def translate(text):
  result = translate_client.translate_text(Text=text, SourceLanguageCode="en", TargetLanguageCode="it")
  tt = result.get('TranslatedText')
  return tt
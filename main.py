import json
import sys
import requests
import os

PIXELFED_HOST = os.environ['PIXELFED_HOST']
PIXELFED_URL = f'https://{PIXELFED_HOST}/api/v1'
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
POSTS_FILE = 'data/content/posts_1.json'

def upload_media(uri):
    media_url = f'{PIXELFED_URL}/media'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Accept': 'application/json'
    }
    files = {
        'file': open('data/' + uri,'rb')
    }
    response = requests.post(media_url, headers=headers, files=files, data={})
    if response.status_code == 200:
        return response.json()['id']
    else:
        print("Failed to upload media.")
        sys.exit(1)

def publish_post(caption, media_ids):
    post_url = f'{PIXELFED_URL}/statuses'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Accept': 'application/json'
    }
    data = {
        'status': caption,
        'media_ids[]': media_ids
    }
    response = requests.post(post_url, headers=headers, data=data)
    if response.status_code == 200:
        print("Post published successfully!")
    else:
        print("Failed to publish post!")
        sys.exit(1)

def main():
    with open(POSTS_FILE, 'r') as file:
        instagram_data = json.load(file)

    instagram_data = sorted(instagram_data, key=lambda x: x['creation_timestamp'])
    instagram_data = instagram_data[9:]
    for item in instagram_data:
        caption = item['title']
        media = item['media']
        media_ids = []

        for image in media:
            image_path = image.get('uri')
            media_ids.append(upload_media(image_path))
        
        publish_post(caption, media_ids)

if __name__ == '__main__':
    main()

import requests
import sqlite3
import time

API_Key = "qPRNpqUB1A7axpBHafC5J1XR"
username = "esmecard"
url = f"https://danbooru.donmai.us/profile.json?api_key={API_Key}/artists/banned"
url = "https://danbooru.donmai.us/posts.json?limit=25&page=3"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:
    posts = response.json()
    for post in posts:
        print({
            'id': post['id'],
            'created_at': post.get('created_at'),
            'score': post.get('score'),
            'rating': post.get('rating'),
            'file_url': post.get('file_url'),
            'tags': post.get('tag_string')
        })
else:
    print("Failed to fetch posts.")
    
print(response.status_code)

print(response.json())
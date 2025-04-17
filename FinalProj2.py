import requests
import sqlite3
import time

API_Key = "qPRNpqUB1A7axpBHafC5J1XR"
username = "esmecard"
url = f"https://danbooru.donmai.us/profile.json?api_key={API_Key}/artists/banned"
url = "https://danbooru.donmai.us/posts.json?limit=25&page=4"

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

#####################################################################

conn = sqlite3.connect("danbooru_posts.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY,
        created_at TEXT,
        score INTEGER,
        rating TEXT,
        file_url TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        post_id INTEGER,
        tag TEXT,
        FOREIGN KEY(post_id) REFERENCES posts(id)
    )
''')

conn.commit()


page = 1
page2 = 2
page3 = 3
page4 = 4
url = f"https://danbooru.donmai.us/posts.json?limit=25&page={page}"
url2 = f"https://danbooru.donmai.us/posts.json?limit=25&page={page2}"
url3 = f"https://danbooru.donmai.us/posts.json?limit=25&page={page3}"
url4 = f"https://danbooru.donmai.us/posts.json?limit=25&page={page4}"
response = requests.get(url)
#response = requests.get(url2)
#response = requests.get(url3)
#response = requests.get(url4)
posts = response.json()


for post in posts:
    post_id = post['id']
    created = post.get('created_at')
    score = post.get('score')
    rating = post.get('rating')
    file_url = post.get('file_url')
    tag_string = post.get('tag_string', '')


    cursor.execute('''
        INSERT OR IGNORE INTO posts (id, created_at, score, rating, file_url)
        VALUES (?, ?, ?, ?, ?)
    ''', (post_id, created, score, rating, file_url))


    for tag in tag_string.split():
        cursor.execute('''
            INSERT INTO tags (post_id, tag)
            VALUES (?, ?)
        ''', (post_id, tag))

conn.commit()
conn.close()

##################################################################################

import csv

conn = sqlite3.connect("danbooru_posts.db")
cursor = conn.cursor()

cursor.execute('''
    SELECT tag, COUNT(*) as count
    FROM tags
    GROUP BY tag
    ORDER BY count DESC
    LIMIT 10
''')
top_tags = cursor.fetchall()


cursor.execute('''
    SELECT rating, AVG(score)
    FROM posts
    GROUP BY rating
''')
avg_scores = cursor.fetchall()


with open("top_tags.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Tag", "Count"])
    writer.writerows(top_tags)
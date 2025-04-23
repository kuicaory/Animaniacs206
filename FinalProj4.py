import sqlite3
import requests
import csv


#Connect to SQLite

conn = sqlite3.connect("anilist_anime.db")
cursor = conn.cursor()

# Create anime table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY,
        title TEXT,
        episodes INTEGER,
        score REAL,
        format TEXT
    )
''')

# Create genres table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anime_id INTEGER,
        genre TEXT,
        FOREIGN KEY(anime_id) REFERENCES anime(id)
    )
''')

conn.commit()

#Fetch from AniList GraphQL API

url = "https://graphql.anilist.co"
query = '''
query ($page: Int, $perPage: Int) {
  Page(page: $page, perPage: $perPage) {
    media(type: ANIME, sort: POPULARITY_DESC) {
      id
      title {
        romaji
      }
      episodes
      averageScore
      format
      genres
    }
  }
}
'''

variables = {
    "page": 1,
    "perPage": 25
}

response = requests.post(url, json={"query": query, "variables": variables})
response.raise_for_status()
anime_batch = response.json()["data"]["Page"]["media"]


# Insert into database

for anime in anime_batch:
    anime_id = anime["id"]
    title = anime["title"]["romaji"]
    episodes = anime.get("episodes")
    score = anime.get("averageScore")
    format_ = anime.get("format")

    print(f"{title} | Episodes: {episodes} | Score: {score} | Format: {format_}")

# Insert into anime table
cursor.execute('''
    INSERT OR IGNORE INTO anime (id, title, episodes, score, format)
    VALUES (?, ?, ?, ?, ?)
''', (anime_id, title, episodes, score, format_))

# Insert genres
for genre in anime.get("genres", []):
    print(f"   ↳ Genre: {genre}")
    cursor.execute('''
        INSERT INTO genres (anime_id, genre)
        VALUES (?, ?)
    ''', (anime_id, genre))

conn.commit()

# Analysis and CSV Export

# Top 10 genres
cursor.execute('''
    SELECT genre, COUNT(*) as count
    FROM genres
    GROUP BY genre
    ORDER BY count DESC
    LIMIT 10
''')
top_genres = cursor.fetchall()

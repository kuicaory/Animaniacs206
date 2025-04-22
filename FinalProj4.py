import requests
import sqlite3
import time

# Connect to SQLite
conn = sqlite3.connect("jikan_anime.db")
cursor = conn.cursor()

# Create anime table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY,
        title TEXT,
        episodes INTEGER,
        score REAL,
        type TEXT
    )
''')

# Create genres table (many-to-one)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anime_id INTEGER,
        genre TEXT,
        FOREIGN KEY(anime_id) REFERENCES anime(id)
    )
''')

conn.commit()

# Function to get anime from API
def fetch_anime_batch(page_num):
    url = f"https://api.jikan.moe/v4/anime?page={page_num}&limit=25"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("data", [])

# Store 25 at a time
page = 1 
anime_batch = fetch_anime_batch(page)

for anime in anime_batch:
    anime_id = anime.get("mal_id")
    title = anime.get("title")
    episodes = anime.get("episodes")
    score = anime.get("score")
    type_ = anime.get("type")

    # PRINT TO TERMINAL
    print(f"{title} | Episodes: {episodes} | Score: {score} | Type: {type_}")

 
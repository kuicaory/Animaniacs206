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

    # Insert into anime table
    cursor.execute('''
        INSERT OR IGNORE INTO anime (id, title, episodes, score, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (anime_id, title, episodes, score, type_))

    # Insert genres with print
    for genre in anime.get("genres", []):
        genre_name = genre.get("name")
        print(f"   ↳ Genre: {genre_name}")
        cursor.execute('''
            INSERT INTO genres (anime_id, genre)
            VALUES (?, ?)
        ''', (anime_id, genre_name))

conn.commit()
conn.close()
print("Batch saved to jikan_anime.db")

############################################################################################

import sqlite3
import csv

conn = sqlite3.connect("jikan_anime.db")
cursor = conn.cursor()

# Top 10 genres
cursor.execute('''
    SELECT genre, COUNT(*) as count
    FROM genres
    GROUP BY genre
    ORDER BY count DESC
    LIMIT 10
''')
top_genres = cursor.fetchall()

# Average score by type
cursor.execute('''
    SELECT type, AVG(score)
    FROM anime
    WHERE score IS NOT NULL
    GROUP BY type
''')
avg_scores = cursor.fetchall()

# Save both to CSV
with open("jikan_top_genres.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Genre", "Count"])
    writer.writerows(top_genres)

with open("jikan_avg_scores_by_type.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Type", "Average Score"])
    writer.writerows(avg_scores)

conn.close()
print("Analysis complete. CSV files saved.")
import sqlite3
import requests

# Connect to or create the SQLite database
conn = sqlite3.connect("tracemoe_anime.db")
cursor = conn.cursor()

# Create table for anime scenes
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anime_title TEXT,
        episode INTEGER,
        similarity REAL,
        timestamp TEXT
    )
''')

# Create table for genres
cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scene_id INTEGER,
        genre TEXT,
        FOREIGN KEY(scene_id) REFERENCES scenes(id)
    )
''')

conn.commit()

# Fetch recent anime scenes from the Trace.moe API
url = "https://api.trace.moe/search?anilistInfo"
response = requests.get(url)
response.raise_for_status()
data = response.json()

# Limit to 25 results
scenes = data["result"][:25]

# Store each scene
for scene in scenes:
    title = scene["anilist"]["title"]["romaji"]
    episode = scene.get("episode")
    similarity = scene.get("similarity")
    timestamp = scene.get("from")  # seconds into the episode

    print(f"🎬 {title} | Ep: {episode} | Confidence: {similarity:.2f} | Time: {timestamp}s")

    # Insert into scenes table
    cursor.execute('''
        INSERT INTO scenes (anime_title, episode, similarity, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (title, episode, similarity, timestamp))

    scene_id = cursor.lastrowid  # Get ID for linking genres

    # Save genres
    for genre in scene["anilist"].get("genres", []):
        print(f"   ↳ Genre: {genre}")
        cursor.execute('''
            INSERT INTO genres (scene_id, genre)
            VALUES (?, ?)
        ''', (scene_id, genre))

conn.commit()
conn.close()
print("Scene batch saved to tracemoe_anime.db")

############################################################################################

import sqlite3
import csv

#this is connecting to the exisiting jikon anime DB
conn = sqlite3.connect("jikan_anime.db")
cursor = conn.cursor()

# getting the top 10 genres and counts how many times each genre appears across all anime
cursor.execute('''
    SELECT genre, COUNT(*) as count
    FROM genres
    GROUP BY genre
    ORDER BY count DESC
    LIMIT 10
''')
top_genres = cursor.fetchall()

# this gets the overall average score for each type like a TV series or movie excluding NULLS
cursor.execute('''
    SELECT type, AVG(score)
    FROM anime
    WHERE score IS NOT NULL
    GROUP BY type
''')
avg_scores = cursor.fetchall()

# Save both to CSV. this file will contain genre name and how many times it appears through it all
with open("jikan_top_genres.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Genre", "Count"])
    writer.writerows(top_genres)

 #this file contains anime type and avg score
with open("jikan_avg_scores_by_type.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Type", "Average Score"])
    writer.writerows(avg_scores)

#closes the DB connection and confirms completion
conn.close()
print("Analysis complete. CSV files saved.")
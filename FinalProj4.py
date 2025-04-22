import requests
import sqlite3
import time

# This connects to or creates the local SQLite file named 'jikan_anime.db'
conn = sqlite3.connect("jikan_anime.db")
cursor = conn.cursor()

# this table stores general anime info from the jikan API
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY,
        title TEXT,
        episodes INTEGER,
        score REAL,
        type TEXT
    )
''')

# this table is storing genres for each anime in the url, linked by anime_id
cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anime_id INTEGER,
        genre TEXT,
        FOREIGN KEY(anime_id) REFERENCES anime(id)
    )
''')

conn.commit()

# I defined the function to to get anime from API
def fetch_anime_batch(page_num):
    url = f"https://api.jikan.moe/v4/anime?page={page_num}&limit=25"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("data", [])

# This function fetches 25 anime from the Jikan API using the given page number ( only doing 1 though)
page = 1 
anime_batch = fetch_anime_batch(page)

for anime in anime_batch:
    anime_id = anime.get("mal_id")
    title = anime.get("title")
    episodes = anime.get("episodes")
    score = anime.get("score")
    type_ = anime.get("type")

    # printed information to the terminal to verify to work
    print(f"{title} | Episodes: {episodes} | Score: {score} | Type: {type_}")

    # inserted anime into the 'anime' table
    cursor.execute('''
        INSERT OR IGNORE INTO anime (id, title, episodes, score, type)
        VALUES (?, ?, ?, ?, ?)
    ''', (anime_id, title, episodes, score, type_))

    # inserted each genre into the 'genres' table
    for genre in anime.get("genres", []):
        genre_name = genre.get("name")
        print(f"   ↳ Genre: {genre_name}")
        cursor.execute('''
            INSERT INTO genres (anime_id, genre)
            VALUES (?, ?)
        ''', (anime_id, genre_name))
#save all insertions to the databases
conn.commit()
#closes the database connections
conn.close()
#this confirms whether the batch was saved
print("Batch saved to jikan_anime.db")

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
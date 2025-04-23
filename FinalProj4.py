import sqlite3
import requests
import csv


#Connect to SQLite

conn = sqlite3.connect("anilist_anime.db")
cursor = conn.cursor()

# Create anime table and includes ID, title, episode count, score, and format
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY,
        title TEXT,
        episodes INTEGER,
        score REAL,
        format TEXT
    )
''')

# Create genres table to store genres
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


# Insert into database. it loops through the anime data

for anime in anime_batch:
    anime_id = anime["id"]
    title = anime["title"]["romaji"]
    episodes = anime.get("episodes")
    score = anime.get("averageScore")
    format_ = anime.get("format")

    print(f"{title} | Episodes: {episodes} | Score: {score} | Format: {format_}")

# Insert into anime table or it ignores it if alreadye exists
cursor.execute('''
    INSERT OR IGNORE INTO anime (id, title, episodes, score, format)
    VALUES (?, ?, ?, ?, ?)
''', (anime_id, title, episodes, score, format_))

# Insert each genre into the genres table linked to the anime
for genre in anime.get("genres", []):
    print(f"   ↳ Genre: {genre}")
    cursor.execute('''
        INSERT INTO genres (anime_id, genre)
        VALUES (?, ?)
    ''', (anime_id, genre))

conn.commit()

# Analysis and CSV Export

# finds the top 10 most common genres across all anime
cursor.execute('''
    SELECT genre, COUNT(*) as count
    FROM genres
    GROUP BY genre
    ORDER BY count DESC
    LIMIT 10
''')
top_genres = cursor.fetchall()

# Average score by format (TV, Movie, etc.)
cursor.execute('''
    SELECT format, AVG(score)
    FROM anime
    WHERE score IS NOT NULL
    GROUP BY format
''')
avg_scores = cursor.fetchall()

# Export genres to CSV file
with open("anilist_top_genres.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Genre", "Count"])
    writer.writerows(top_genres)

# Export average scores by format to a CSV file
with open("anilist_avg_scores_by_format.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Format", "Average Score"])
    writer.writerows(avg_scores)

# Done for final confirmation and cleanup
conn.close()
print("Data saved and CSV files generated:")
print(" - anilist_top_genres.csv")
print(" - anilist_avg_scores_by_format.csv")
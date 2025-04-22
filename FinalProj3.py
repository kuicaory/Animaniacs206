import requests
import sqlite3

def top_animes():
    conn3 = sqlite3.connect('anime_quotes.db')
    cur = conn3.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS animes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_id INTEGER UNIQUE,
            anime_name TEXT,
            rating INTEGER,
            rank INTEGER,
            year INTEGER
        )
    """)
    conn3.commit()

    anime_set = set()
    page = 1

    while len(anime_set) < 1:
        third_url = f'https://api.jikan.moe/v4/top/anime?page={page}'
        try:
            resp = requests.get(third_url)
            if resp.status_code == 200:
                data3 = resp.json()
                for anime in data3['data']:
                    if anime['mal_id'] not in anime_set and len(anime_set) < 25:
                        cur.execute("SELECT 1 FROM animes WHERE anime_id = ?", (anime['mal_id'],))
                        if cur.fetchone():
                            continue
                        cur.execute("""
                            INSERT OR IGNORE INTO animes (anime_id, anime_name, rating, rank, year)
                            VALUES (?, ?, ?, ?, ?)
                            """, (
                                anime['mal_id'],
                                anime['title'],
                                anime.get('score', None),
                                anime.get('rank', None),
                                anime.get('year', None)
                            ))
                        conn3.commit()
                        anime_set.add(anime['mal_id'])
                        print(f"Added Rank {anime.get('rank')}: {anime['title']}")
            else:
                print(f"Failed to fetch page {page} — status code {resp.status_code}")
            page += 1
        except Exception as e:
            print(f'Error on page {page}', e) 
    conn3.close()

def main():
    top_animes()
main()

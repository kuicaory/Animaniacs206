import requests
import sqlite3

def top_animes():
    conn3 = sqlite3.connect('anime-list')
    cur = conn3.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS animes (
            id INTEGER PRIMARY KEY,
            anime_id INTEGER,
            anime_name TEXT,
            rating INTEGER,
            rank INTEGER,
            year INTEGER
        )
    """)
    conn3.commit()
    third_url = 'https://api.jikan.moe/v4/top/anime'
    # anime_set = set()
    # while len(anime_set) < 15:
        # try:
    resp = requests.get(third_url)
    if resp.status_code == 200:
        data3 = resp.json()
        print(data3)
        #content = da
        # except:
        #     return None

def main():
    top_animes()
main()
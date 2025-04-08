import requests
import sqlite3
import time

conn = sqlite3.connect('anime_quotes.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        anime_id INTEGER,
        anime_name TEXT,
        anime_alt_name TEXT,
        character_id INTEGER,
        character_name TEXT,
        quote TEXT
    )
''')
conn.commit()

url = "https://api.animechan.io/v1/quotes/random"
quote_set = set()

while len(quote_set) < 10:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            content = data['data']['content']
            anime = data['data']['anime']
            character = data['data']['character']

            quote_key = (anime['id'], character['id'], content)
            if quote_key not in quote_set:
                quote_set.add(quote_key)
                cursor.execute('''
                    INSERT INTO quotes (
                        anime_id, anime_name, anime_alt_name,
                        character_id, character_name, quote
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    anime['id'], anime['name'], anime.get('altName', ''),
                    character['id'], character['name'], content
                ))
                print(f"[{len(quote_set)}] {character['name']}: \"{content}\"")
        else:
            print("Failed request. Status code:", response.status_code)
        time.sleep(0.2)
    except Exception as e:
        print("Error:", e)

conn.commit()
conn.close()
print("✅ Done: 10 quotes saved to 'anime_quotes.db'")

API_Key = "qPRNpqUB1A7axpBHafC5J1XR"
url = f"https://danbooru.donmai.us/profile.json?api_key={API_Key}"
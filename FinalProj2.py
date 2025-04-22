import requests
from bs4 import BeautifulSoup
import sqlite3

DB_NAME = "anime_quotes.db"

def create_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS anime_titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            score REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_title(title, score):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT OR IGNORE INTO anime_titles (title, score) VALUES (?, ?)", (title, score))
        conn.commit()
    finally:
        conn.close()

def scrape_page(page_num=1, half=1):
    """
    page_num: 1 = 0 offset, 2 = 50 offset, etc.
    half: 1 = top 25, 2 = bottom 25
    """
    offset = (page_num - 1) * 50
    url = f"https://myanimelist.net/topanime.php?type=bypopularity&limit={offset}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to load page {page_num}. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    entries = soup.select("tr.ranking-list")

    # Only take 25 at a time
    if half == 1:
        entries = entries[:25]
    else:
        entries = entries[25:]

    print(f"Scraping page {page_num}, half {half} (entries {1 if half == 1 else 26}–{25 if half == 1 else 50})")

    for entry in entries:
        title_tag = entry.select_one("h3.anime_ranking_h3 a")
        score_tag = entry.select_one("td.score span.score-label")

        if title_tag and score_tag:
            title = title_tag.text.strip()
            score = score_tag.text.strip()
            score_val = float(score) if score != "N/A" else None

            insert_title(title, score_val)
            print(f"Added: {title} | Score: {score}")

if __name__ == "__main__":
    create_table()

    try:
        page = int(input("Enter the page number to scrape (1 = top 50, 2 = 51–100, etc.): "))
        half = int(input("Enter 1 to scrape top 25 or 2 for bottom 25 of the page: "))
        if half not in (1, 2):
            raise ValueError
        scrape_page(page, half)
    except ValueError:
        print("Invalid input. Page must be int, and half must be 1 or 2.")

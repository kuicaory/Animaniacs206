import sqlite3
import matplotlib.pyplot as plt
from collections import defaultdict

def get_quote_counts(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Count quotes per anime, joining with animes table to get ranking
    cur.execute('''
        SELECT q.anime_name, COUNT(*) AS quote_count, a.rank
        FROM quotes q
        JOIN animes a ON q.anime_name = a.anime_name
        WHERE a.rank IS NOT NULL
        GROUP BY q.anime_name
        ORDER BY quote_count DESC
    ''')

    results = cur.fetchall()
    conn.close()

    return results

def plot_quote_counts(data):
    anime_names = [f"{anime} (#{rank})" for anime, _, rank in data]
    quote_counts = [count for _, count, _ in data]

    plt.figure(figsize=(12, 6))
    plt.barh(anime_names, quote_counts, color='lightcoral', edgecolor='black')
    plt.xlabel("Number of Quotes")
    plt.title("Number of Quotes per Anime (with Rankings)")
    plt.gca().invert_yaxis()  # Highest quote count on top
    plt.tight_layout()
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

# Usage
db_path = "anime_quotes.db"  # Replace with your actual DB path
quote_data = get_quote_counts(db_path)
plot_quote_counts(quote_data)

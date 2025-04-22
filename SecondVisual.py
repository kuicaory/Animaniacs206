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

def write_quote_counts_to_txt(data, filename="quote_counts_by_rank.txt"):
    # Sort by descending rank (i.e., rank 1000 -> 1 becomes ascending numerically)
    sorted_data = sorted(data, key=lambda x: x[2], reverse=False)

    with open(filename, "w", encoding="utf-8") as f:
        for anime, count, rank in sorted_data:
            f.write(f"{anime} (Rank #{rank}): {count} quotes\n")

    print(f"Data written to {filename}")


db_path = "anime_quotes.db"
quote_data = get_quote_counts(db_path)
write_quote_counts_to_txt(quote_data)
plot_quote_counts(quote_data)


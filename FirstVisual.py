import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt

def group_animes_by_year(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT year FROM animes WHERE year IS NOT NULL")
    years = [row[0] for row in cur.fetchall()]

    year_groups = defaultdict(int)
    for year in years:
        year_groups[year] += 1

    conn.close()

    return dict(sorted(year_groups.items()))

def plot_year_distribution(grouped_data):
    labels = list(map(str, grouped_data.keys()))
    values = list(grouped_data.values())

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color='violet', edgecolor='black')
    plt.xlabel('Year')
    plt.ylabel('Number of Animes')
    plt.title('Anime Counts by Year')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def write_data_to_file(grouped_data, filename="counts.txt"):
    with open(filename, 'w') as f:
        for year, count in grouped_data.items():
            f.write(f"{year}: {count} animes\n")
    print(f"Data written to {filename}")


db_path = "anime_quotes.db"
grouped = group_animes_by_year(db_path)
write_data_to_file(grouped)
plot_year_distribution(grouped)

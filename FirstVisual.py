import sqlite3
from collections import defaultdict
import matplotlib.pyplot as plt

def get_half_decade_range(year):
    """Returns the start of the half-decade range the year belongs to."""
    return year - (year % 5)

def group_animes_by_half_decade(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT year FROM animes WHERE year IS NOT NULL")
    years = [row[0] for row in cur.fetchall()]

    half_decade_groups = defaultdict(int)
    for year in years:
        start = get_half_decade_range(year)
        end = start + 4
        label = f"{start}-{end}"
        half_decade_groups[label] += 1

    conn.close()

    return dict(sorted(half_decade_groups.items()))

def plot_half_decade_distribution(grouped_data):
    labels = list(grouped_data.keys())
    values = list(grouped_data.values())

    plt.figure(figsize=(12, 6))
    plt.bar(labels, values, color='violet', edgecolor='black')
    plt.xlabel('Half-Decade Range')
    plt.ylabel('Number of Animes')
    plt.title('Anime Counts by Half-Decade')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def write_data_to_file(grouped_data, filename="half_decade_counts.txt"):
    with open(filename, 'w') as f:
        for range_label, count in grouped_data.items():
            f.write(f"{range_label}: {count} animes\n")
    print(f"Data written to {filename}")


db_path = "anime_quotes.db"
grouped = group_animes_by_half_decade(db_path)
write_data_to_file(grouped)
plot_half_decade_distribution(grouped)


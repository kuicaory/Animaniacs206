import sqlite3
import matplotlib.pyplot as plt

def plot_anime_format_distribution(db_path='anilist_anime.db', output_file='format_distribution.txt'):
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

     # Count number of anime for each format
    cursor.execute('''
        SELECT format, COUNT(*) as count
        FROM anime
        WHERE format IS NOT NULL
        GROUP BY format
    ''')
    data = cursor.fetchall()
    conn.close()

    # Write data to a text file
    with open(output_file, 'w') as f:
        f.write("Format\tCount\n")
        for format_, count in data:
            f.write(f"{format_}\t{count}\n")

    # Prepare data for pie chart
    formats = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Plot the pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=formats, autopct='%1.1f%%', startangle=140, shadow=True)
    plt.title("Distribution of Anime Formats (TV, Movie, OVA, etc.)")
    plt.tight_layout()
    plt.show()

# Run it
plot_anime_format_distribution('anilist_anime.db')
   
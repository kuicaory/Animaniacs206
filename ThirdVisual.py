import sqlite3
import matplotlib.pyplot as plt

def plot_quotes_per_anime(db_path='your_database.db', output_file='quotes_per_anime.txt'):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    SELECT at.id, at.title, COUNT(*) as quote_count
    FROM quotes q
    JOIN anime_titles at ON q.anime_name = at.title
    GROUP BY at.id, at.title
    ORDER BY at.id
    """

    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()

    # Write to text file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Anime ID\tAnime Title\tQuote Count\n")
        for anime_id, title, count in data:
            f.write(f"{anime_id}\t{title}\t{count}\n")

    # Prepare data for plotting
    titles = [row[1] for row in data]
    counts = [row[2] for row in data]

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.barh(titles[::-1], counts[::-1], color='teal')
    plt.title("Anime Quote Counts (Sorted by Anime ID)")
    plt.xlabel("Number of Quotes")
    plt.ylabel("Anime Title")
    plt.tight_layout()
    plt.show()

plot_quotes_per_anime('anime_quotes.db')

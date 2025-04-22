import sqlite3
import matplotlib.pyplot as plt

def plot_anime_titles_by_year(db_path='your_database.db', output_file='anime_year_data.txt'):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to join and count by year
    query = """
    SELECT a.year, COUNT(*) as count
    FROM anime_titles at
    JOIN animes a ON at.title = a.anime_name
    WHERE a.year IS NOT NULL
    GROUP BY a.year
    ORDER BY a.year
    """
    cursor.execute(query)
    data = cursor.fetchall()

    # Close DB connection
    conn.close()

    # Write data to text file
    with open(output_file, 'w') as f:
        f.write("Year\tCount\n")
        for year, count in data:
            f.write(f"{year}\t{count}\n")

    # Prepare data for plotting
    years = [row[0] for row in data]
    counts = [row[1] for row in data]

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(years, counts, marker='o', linestyle='-', color='skyblue')
    plt.title("Number of Anime Titles by Release Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Matching Titles")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_anime_titles_by_year('anime_quotes.db')

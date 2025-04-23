import sqlite3
import matplotlib.pyplot as plt

def plot_anime_format_distribution(db_path='anilist_anime.db', output_file='format_distribution.txt'):
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

   
import sqlite3
import requests
import csv


#Connect to SQLite

conn = sqlite3.connect("anilist_anime.db")
cursor = conn.cursor()

# Create anime table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY,
        title TEXT,
        episodes INTEGER,
        score REAL,
        format TEXT
    )
''')
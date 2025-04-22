import requests
import sqlite3
import time

# Connect to SQLite
conn = sqlite3.connect("jikan_anime.db")
cursor = conn.cursor()

# Create anime table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS anime (
        id INTEGER PRIMARY KEY,
        title TEXT,
        episodes INTEGER,
        score REAL,
        type TEXT
    )
''')
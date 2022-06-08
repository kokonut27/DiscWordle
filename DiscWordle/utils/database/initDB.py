import sqlite3 

connection = sqlite3.connect('DiscWordle/utils/database/database.db')

with open('DiscWordle/utils/database/schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO wordles (creator, word, topic) VALUES (?, ?, ?)", (921548675119992852, "disco", "music"))

connection.commit()
connection.close()
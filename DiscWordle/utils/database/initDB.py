import sqlite3 

connection = sqlite3.connect('DiscWordle/utils/database/database.db')

with open('DiscWordle/utils/database/schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO wordles (word, topic) VALUES (?, ?)", ("disco", "music"))

connection.commit()
connection.close()
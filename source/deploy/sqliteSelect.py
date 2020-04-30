 
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('SELECT * FROM measurements')
print(c.fetchall()) 

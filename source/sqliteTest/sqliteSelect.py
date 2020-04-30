 
import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

c.execute('SELECT * FROM measurements')
print(c.fetchone()) 

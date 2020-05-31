 
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('''CREATE TABLE measurements
             (source text, team_name text, created_on_timestamp real, temperature real)''')

conn.commit()
conn.close()
 

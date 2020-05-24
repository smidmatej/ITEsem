 
import sqlite3
#(source text, team_name text, created_on_timestamp real, temperature real)
conn = sqlite3.connect('data.db')
c = conn.cursor()

c.execute('SELECT * FROM measurements WHERE team_name = "blue" AND temperature NOT BETWEEN 0 AND 25')
print(c.fetchall()) 

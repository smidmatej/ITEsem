 
import sqlite3

conn = sqlite3.connect('example.db')
c = conn.cursor()

c.execute('''CREATE TABLE measurements
             (createdOn text, sensorUUID text, temperature real, status text)''')

conn.commit()
conn.close()

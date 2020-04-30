 
 
import sqlite3


time =  '2020-04-28T20:48:54.850744'
sensorUUIDblue = 'd384a529-6227-4133-afc9-4f5a16665f1f'
temperature = 22.200536974016668
status = 'TEST'

conn = sqlite3.connect('example.db')
c = conn.cursor()



c.execute("INSERT INTO measurements VALUES (?,?,?,?)", (time, sensorUUIDblue, temperature, status))

conn.commit()
conn.close()

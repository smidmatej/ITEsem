 
import sqlite3
import time
#(source text, team_name text, created_on_timestamp real, temperature real)


def get_history(team_name):

    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    time_now = time.time() #momentalni epoch time
    time_24h = 24*60*60 # pocet sekund ve 24hodinach
    time_minus_24h = time_now - time_24h

    
    #od nejmladsiho do nejstarsiho
    cursor.execute('SELECT temperature, created_on_timestamp FROM measurements WHERE team_name = (?) AND created_on_timestamp > (?) ORDER BY created_on_timestamp', (team_name, time_minus_24h))
    output = cursor.fetchall()

    x = [item[1] for item in output] #casove hodnoty
    y = [item[0] for item in output] #teplotni hodnoty

    return {'x': x, 'y': y} 


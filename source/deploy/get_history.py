#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import time
from get_stats import get_stats
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


def get_most_recent_db_entry_for_team(team_name):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    STATE = dict()
    cursor.execute('SELECT * FROM measurements WHERE team_name = (?) ORDER BY created_on_timestamp DESC LIMIT 1', (team_name,))
    entry = cursor.fetchall()[0]
    stats = get_stats(team_name)
    team_state = {'team': team_name, 'Status': 'Online', 'cur_temp': entry[3], 'min_temp': stats[0], 'max_temp': stats[1], 'avg_temp': stats[2]}
    return team_state

if __name__ == "__main__":
    most_recent_db_entry_for_each_team()
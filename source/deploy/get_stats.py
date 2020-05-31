#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3
from datetime import datetime
import time
from statistics import mean

def get_stats(team):
    """Pro tým zadaný v argumentu zjistí z databáze průměrnou, maximální a minimální teplotu za posledních 24 hodin"""
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()


    time_now = time.time() #momentalni epoch time
    time_24h = 24*60*60 # pocet sekund ve 24hodinach
    time_minus_24h = time_now - time_24h
    
    cursor.execute('SELECT temperature, created_on_timestamp FROM measurements WHERE team_name = (?) AND created_on_timestamp > (?) ORDER BY created_on_timestamp', (team, time_minus_24h))
    output = cursor.fetchall() #casove hodnoty
    if output == []: #prazdna databaze
        temperatures = [-1000]
    else:
        temperatures = [item[0] for item in output] #teplotni hodnoty

    '''
    ## Provedení statistik
    
    #team min temp
    team_min = min(temperatures)

    #team max temp
    team_max = max(temperatures)

    #team avg temp
    team_avg = mean(temperatures)
    
    
    return [team_min, team_max, team_avg]

if __name__ == "__main__":
    get_stats("blue")

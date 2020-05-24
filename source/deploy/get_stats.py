#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3
from datetime import datetime
import time
from statistics import mean

def get_stats(team):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()


    today = str(datetime.now().date().day)
    if len(today) == 1:
        today = '0' + today

    this_month = str(datetime.now().date().month)
    if len(this_month) == 1:
        this_month = '0' + this_month


    # list tuplů (čas, teplota) z databáze
    team_temptime = c.execute('SELECT temperature, created_on_timestamp FROM measurements WHERE team_name = (?)',(team,)).fetchall()

    # převedení času na použitelné hodnoty
    team_data = []
    for i in range(0,len(team_temptime)): 
        team_data.append((team_temptime[i][0],time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(team_temptime[i][1]))))    
    
    # zjištění dnešních teplot
    valid_team_data = []
    for i in range(0,len(team_data)):
        if team_data[i][1][5:7] == this_month and team_data[i][1][8:10] == today:
            valid_team_data.append(team_data[i])    

    # oddělení dnešních teplot
    team_temp_valid = []
    for i in range(0,len(valid_team_data)):
        team_temp_valid.append(valid_team_data[i][0])

    ## Provedení statistik
    
    #team min temp
    team_min = min(team_temp_valid)

    #team max temp
    team_max = max(team_temp_valid)

    #team avg temp
    team_avg = mean(team_temp_valid)
    
    
    return [team_min, team_max, team_avg]

#name = 'blue'
#stats = get_stats(name)
#print(stats)

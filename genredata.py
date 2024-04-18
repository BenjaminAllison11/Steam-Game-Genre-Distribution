import os
from time import sleep
from giantbomb import giantbomb
from steam_web_api import Steam
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import json
import requests
from collections import Counter
KEY=os.getenv("STEAM_API_KEY") #retrieves your steam api key from your env file
gb = giantbomb.Api('API CODE HERE', 'API test')#Enter giant bomb api code here. I tried to place it in the env file, but it didn't work

load_dotenv()
delay = 10 #the delay is needed so that you don't run out of requests

steam= Steam(KEY)
Steam_Code=input("Enter your steam ID here: ")

user = steam.users.get_owned_games(Steam_Code)
userGames = []
gameID= []
gameGenre = []
def getSteamGames():  #gets user's steam games with steam api
    for game in user['games']:
        gameName = game['name']
        print(gameName)
        userGames.append(gameName)
    with open('steamgamelist', 'a+', encoding='utf-8') as gamelist:
        for game in userGames:
         gamelist.write(game + "\n")
    gamelist.close

def getGameID(): #reads the text file made from getSteamGames(), cross references the giant bomb api using the steam game name, and returns the giantbomb api ids in a string format
    with open('steamgamelist', 'r', encoding='utf-8') as gamelist:
        with open('gameidlist', 'a+', encoding='utf-8') as idlist:
            for gameName in gamelist:
                    try:
                        result = gb.search(gameName)
                        if result:  
                            gameID.append(result[0].id)
                            print(result[0].id)
                            sleep(delay)
                        else:
                            print(f"Game '{gameName}' not found on Giant Bomb.")
                    except requests.exceptions.JSONDecodeError:
                        print(f"Error processing Giant Bomb response for '{gameName}'.")
                    for id in gameID:
                        idlist.write(str(id) + "\n")
        idlist.close
    gamelist.close
print(gameID)
def getGameGenre(): #uses the giantbomb api to retrieve the genres of each ids and writes it to a new file
    with open('gameidlist', 'r', encoding='utf-8') as idlist:
        with open('genrelist', 'a+', encoding='utf-8') as genrelist:
            for id in idlist:
                    id = int(id)
                    result = gb.get_game(id)
                    if result.genres is not None:
                        for genre in result.genres:
                            gameGenre.append(genre.name)
                            print(genre.name)
                            sleep(delay)
                    else:
                        print(f"Error processing genre for {id}")
            for genre in gameGenre:
                genrelist.write(str(genre) + "\n")
        genrelist.close()   
        idlist.close()

def createCharts(): #uses matplotlib to read the list of genres, then returns the number of time each genre occurs
    genre_counts = {}  # Dictionary to store genre counts
    with open('genrelist', 'r', encoding='utf-8') as genrelist:
        for line in genrelist:
            genre = line.strip()  
            genre_counts[genre] = genre_counts.get(genre, 0) + 1  
    genre_labels = list(genre_counts.keys())  
    genre_values = list(genre_counts.values()) 
    fig = plt.figure(figsize=(200,200))
    plt.pie(genre_values, labels=genre_labels, autopct='%.2f')
    plt.show()
        



getSteamGames()
getGameID()
getGameGenre()
createCharts()
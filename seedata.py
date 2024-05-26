import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json

def genreDistribution():  
    genresCount= {}
    with open('gameData', 'r', encoding='utf-8') as gameData:
        game_data = json.load(gameData)
    for game in game_data:
        genres = game['Genres']
        for genre in genres:
            genresCount[genre] = genresCount.get(genre, 0) + 1 
    genre_labels = list(genresCount.keys())  
    genre_values = list(genresCount.values()) 
    fig = plt.figure(figsize=(200,200))
    plt.pie(genre_values, labels=genre_labels, autopct='%.2f')
    plt.show()


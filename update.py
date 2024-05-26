import os
from giantbomb import giantbomb
from steam_web_api import Steam
from dotenv import load_dotenv
import requests
import json
from time import sleep
KEY=os.getenv("STEAM_API_KEY")
gb = giantbomb.Api('API KEY HERE', 'API test')
steam= Steam(KEY)
load_dotenv()
delay = 20
user = steam.users.get_owned_games('put steam id here')


def update():
    print("Updating Game Library")
    gameList = []
    newGames = []
    with open('gameData', 'r', encoding='utf-8') as gameData:  
        game_data = json.load(gameData)  
        for game in game_data:
            gameList.append(game['Game Name'])
    for game in user['games']:
       if game['name'] not in gameList:
            gameInfo = {}
            gameGenres=[]
            gameInfo['Game Name'] = game['name']
            gameInfo['Play Time'] = game['playtime_forever']
            gameInfo['Steam ID'] = game['appid']
            try:
                result=gb.search(game['name'])
                if result:
                    id = result[0].id
                    gameInfo['GiantBomb ID'] = id
                    gameResults = gb.get_game(id)
                    if gameResults.genres is not None:
                        for genre in gameResults.genres:
                            gameGenres.append(genre.name)
                    else:
                        print(f"Error processing genre for {id}")
                else:
                    print(f"Game '{game['name']}' not found on Giant Bomb.")
            except requests.exceptions.JSONDecodeError:
                print(f"Error processing Giant Bomb response for '{game['name']}'.")
            gameInfo['Genres']=gameGenres
            newGames.append(gameInfo)
            sleep(delay)
            print(gameInfo)
    with open('gameData', 'r', encoding='utf-8') as gameData:  
        game_data=json.load(gameData)
        updatedData=game_data+newGames
        with open('gameData', 'w', encoding='utf-8') as gameData:
            json.dump(updatedData, gameData, indent=4)
    print('Update Complete')


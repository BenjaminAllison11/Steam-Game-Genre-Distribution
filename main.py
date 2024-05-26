from makelibrary import getGameInfo
from seedata import genreDistribution 
from update import update

def start():
    while True:
        print("What would you like to do? 1. Get your library information 2. Update your library information 3. See data 4. Quit")
        choice = input()
        if choice == '1':
            getGameInfo()
        elif choice == '2':
            update()
        elif choice == '3':
            genreDistribution()
        elif choice == '4':
            break
        else:
            print('Please choose choices 1, 2, 3, or 4')
            start()



start()
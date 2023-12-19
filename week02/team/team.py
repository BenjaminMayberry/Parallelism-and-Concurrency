"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from concurrent.futures import thread
from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    def __init__(self, url):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.url = url
        self.response = {}

    def run(self):
        response = requests.get(self.url)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('responce if here probaly failed = ', response.status_code)
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        get = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/shuffle/')
        get.start()
        get.join()
        print(get.response)
        self.remaining = 52
        

    def draw_card(self):
        get = Request_thread(rf'https://deckofcardsapi.com/api/deck/{self.id}/draw/?count=1')
        get.start()
        get.join()
        self.remaining -= 1
        #print (get.response)
        card = str(get.response["cards"][0]["value"]) + " of " + str(get.response["cards"][0]["suit"])
        return card


    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = 'kseikd5i3hgd'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<


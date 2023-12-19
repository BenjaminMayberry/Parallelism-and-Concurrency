"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 05 Team Activity

Instructions:

- Make a copy of your assignment 2 program.  Since you are working in a team,
  you can design which assignment 2 program that you will use for the team
  activity.
- Convert the program to use a process pool and use apply_async() with a
  callback function to retrieve data from the Star Wars website.

"""

"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from ast import Global
from datetime import datetime, timedelta
from pickle import NONE
from pandas import concat
from pyparsing import null_debug_action
import requests
import json
import threading
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0
result_list = []

# TODO Add your threaded class definition here
class Request_thread(threading.Thread):
    def __init__(self, call):
        # Call the Thread class's init function
        threading.Thread.__init__(self)
        self.call = call
        self.response = {}

    def run(self):
        global call_count
        response = requests.get(self.call)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            self.response = response.json()
        else:
            print('responce if here probaly failed = ', response.status_code)
        call_count += 1

def request(call):

        global call_count
        response = requests.get(call)
        # Check the status code to see if the request succeeded.
        if response.status_code == 200:
            response = response.json()
        else:
            print('responce if here probaly failed = ', response.status_code)
        call_count += 1
        return response


# TODO Add any functions you need here
def print_data(log, data_set, data_type):
  data1 = len(data_set)
  log.write(f'{data_type}: {data1}')
  last = data_set[int(len(data_set) - 1)]
  all_in_one_line = ""
  for i in data_set:
    if i == last:
      #print("done")
      all_in_one_line += i
    else:
      #print("not done")
      all_in_one_line += i + ", "
  log.write(all_in_one_line)

def collect_names(data_set):
  pass
def log_result(result):
  result_list.append(result)

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')
    
    # TODO Retrieve Top API urls
    top_api_call = Request_thread(rf'{TOP_API_URL}')
    top_api_call.start()
    top_api_call.join()
    #print(top_api_call.response)
    # TODO Retireve Details on film 6
    films_call = top_api_call.response["films"]
    films_call = films_call+"6"
    #print(films_call)
    films = Request_thread(rf'{films_call}')
    films.start()
    films.join() 
    #print (films.response) 
    # TODO Display results
    Characters = []
    Planets = []
    Starships = []
    Vehicles = []
    Species = []

    for chare in films.response["characters"]:
      Characters.append(chare)

    for plan in films.response["planets"]:
      Planets.append(plan)

    for star in films.response["starships"]:
      Starships.append(star)

    for vec in films.response["vehicles"]:
      Vehicles.append(vec)

    for spe in films.response["species"]:
      Species.append(spe)

    Characters_Hit = []
    Planets_Hit = []
    Starships_Hit = []
    Vehicles_Hit = []
    Species_Hit = []
    

    pool = mp.Pool(4)
    results = [pool.apply_async(request, args=(address, )) for address in Characters]
        # do something else

    # collect all of the results into a list
    Characters_Hit = [p.get() for p in results]
    pool.close()
    pool.join()
    
    # for address in Characters:
    #   Characters_Hit.append(Request_thread(rf'{address}'))
    
    for address in Planets:
      Planets_Hit.append(Request_thread(rf'{address}'))

    for address in Starships:
      Starships_Hit.append(Request_thread(rf'{address}'))

    for address in Vehicles:
      Vehicles_Hit.append(Request_thread(rf'{address}'))

    for address in Species:
      Species_Hit.append(Request_thread(rf'{address}'))

    # for hit in Characters_Hit:
    #   hit.start()
    for hit in Planets_Hit:
      hit.start()
    for hit in Starships_Hit:
      hit.start()
    for hit in Vehicles_Hit:
      hit.start()
    for hit in Species_Hit:
      hit.start()

    
    Characters_Names = []
    Planets_Names = []
    Starships_Names = []
    Vehicles_Names = []
    Species_Names = []
    
    pool = mp.Pool(4)

    

    for hit in Characters_Hit:
      #hit.join()
      Characters_Names.append(hit["name"])

    



    for hit in Planets_Hit:
      hit.join()
      Planets_Names.append(hit.response["name"])

    for hit in Starships_Hit:
      hit.join()
      Starships_Names.append(hit.response["name"])

    for hit in Vehicles_Hit:
      hit.join()
      Vehicles_Names.append(hit.response["name"])

    for hit in Species_Hit:
      hit.join()
      Species_Names.append(hit.response["name"])
    title = "Title   : ", films.response["title"]
    director = "Director: ", films.response["director"]
    producer = "Producer: ", films.response["producer"]
    relese_date = "Released: ", films.response["release_date"]
    
    log.write(f'Title   : {films.response["title"]}')
    log.write(f'Director: {films.response["director"]}')
    log.write(f'Producer: {films.response["producer"]}')
    log.write(f'Released: {films.response["release_date"]}\n')
    

    Characters_Names.sort()
    Planets_Names.sort()
    Starships_Names.sort()
    Vehicles_Names.sort()
    Species_Names.sort()


    print_data(log, Characters_Names, "Characters")
    log.write("")
    print_data(log, Planets_Names, "Planets")
    log.write("")
    print_data(log, Starships_Names, "Starships")
    log.write("")
    print_data(log, Vehicles_Names, "Vehicles")
    log.write("")
    print_data(log, Species_Names, "Species")
    log.write("")


    


    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()

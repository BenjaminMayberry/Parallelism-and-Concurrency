"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

from logging import critical
import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    print(STARTING_CLEANING_MESSAGE)
    time.sleep(random.uniform(0, 2))
    print(STOPPING_CLEANING_MESSAGE)

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

def cleaner(id, start_time, clean_lock, party_lock, Cleaned_Times):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    #print(f"cleaner {id}")
    while (start_time + TIME) > time.time():
        Room_Party_Lock = clean_lock.acquire(True, 1)
        Room_Clean_Lock = party_lock.acquire(True, 1)
        if Room_Party_Lock and Room_Clean_Lock:
            cleaner_cleaning(id)
            Cleaned_Times.value += 1

            
            party_lock.release()
            clean_lock.release()
            cleaner_waiting()
        elif Room_Party_Lock:
            clean_lock.release()
        elif Room_Clean_Lock:
            party_lock.release()
        
        
    
    #cleaner_cleaning()
    
    pass

def guest(id, start_time, party_lock, Party_Pepole_Count, critical, Party_Times):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    # print(f"guest {id}")
    while (start_time + TIME) > time.time():
        Room_Party_Lock = party_lock.acquire(True, 1)
        critical.acquire()
        if Room_Party_Lock or Party_Pepole_Count.value > 0:
            
            Party_Pepole_Count.value += 1
            critical.release()
            if Room_Party_Lock:
                print(STARTING_PARTY_MESSAGE)
            
            guest_partying(id)
            critical.acquire()
            Party_Pepole_Count.value -= 1
            critical.release()
            if Party_Pepole_Count.value == 0:

                print(STOPPING_PARTY_MESSAGE)
                Party_Times.value += 1

                party_lock.release()
            else:
                # print(f"Number of pepole left partying {Party_Pepole_Count.value}")
                pass
            guest_waiting()
        else:
            critical.release()    
        
        # Room_Party_Lock = clean_lock.acquire(True, 1)
        # Room_Clean_Lock = party_lock.acquire(True, 1)
        # if Room_Party_Lock and Room_Clean_Lock:
        #     cleaner_cleaning(id)
        #     clean_lock.release()
        #     party_lock.release()
        #     cleaner_waiting()
        # elif Room_Party_Lock:
        #     clean_lock.release()
        # elif Room_Clean_Lock:
        #     party_lock.release()

    pass

def main():
    # Start time of the running of the program. 
    start_time = time.time()
    
    
    # print(time.time())
    # Cleaned_Times = mp.RawValue('i', 0)
    # Party_Times = mp.RawValue('i', 0)
    Party_Pepole_Count = mp.RawValue('i', 0)
    Cleaned_Times = mp.RawValue('i', 0)
    Party_Times = mp.RawValue('i', 0)
    pepole = []
    clean_lock = mp.Lock()
    party_lock = mp.Lock()
    critical = mp.Lock()

    # TODO - add any variables, data structures, processes you need
    # TODO - add any arguments to cleaner() and guest() that you need
    
    c1 = mp.Process(target=cleaner, args=(1, start_time, clean_lock, party_lock, Cleaned_Times))
    pepole.append(c1)

    g1 = mp.Process(target=guest, args=(1, start_time, party_lock, Party_Pepole_Count, critical, Party_Times))
    pepole.append(g1)


    for x in range(CLEANING_STAFF - 1):
      g1 = mp.Process(target=cleaner, args=((x + 2), start_time, clean_lock, party_lock, Cleaned_Times))
      pepole.append(g1)

    for x in range(HOTEL_GUESTS  - 1):
      c1 = mp.Process(target=guest, args=((x + 2), start_time, party_lock, Party_Pepole_Count, critical, Party_Times))
      pepole.append(c1)
    # TODO - Start the processes and wait for them to finish
    for i in pepole:
      i.start()

    for i in pepole:
      i.join()

    # Results
    print(f'Room was cleaned {Cleaned_Times.value} times, there were {Party_Times.value} parties')


if __name__ == '__main__':
    main()
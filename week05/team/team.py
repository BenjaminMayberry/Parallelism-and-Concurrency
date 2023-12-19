"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread/process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random

#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def file_reader(filename, queue_of_data, PoolSize): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """
    
    with open(filename) as f:
        for line in f:
            contents = line
            queue_of_data.put(int(contents))
    
    for i in range(0, PoolSize):
        queue_of_data.put("NO_MORE_VALUES")
    print("Done")

# TODO create prime_process function
def prime_process(queue_of_data, primes):
    while True:
        Calculate = queue_of_data.get()
        if Calculate != "NO_MORE_VALUES":      
            if is_prime(Calculate):
                primes.append(Calculate)
        else:
            print("Thread Done")
            break



def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(100000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')
    print("Done")


def main():
    """ Main function """

    filename = 'data.txt'
    PoolSize = PRIME_PROCESS_COUNT

    # Once the data file is created, you can comment out this line
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    Calculateifprime = mp.Manager().Queue()
    primes = mp.Manager().list()
    # TODO create reading thread
    read = threading.Thread(target=file_reader, args=(filename, Calculateifprime, PoolSize))
    # TODO create prime processes
    PrimeProsseses = []
    for i in range(0, PoolSize):
        pool = mp.Process(target=prime_process, args=(Calculateifprime, primes))
        PrimeProsseses.append(pool)
    # TODO Start them all
    read.start()
    for p in PrimeProsseses:
        p.start()
    numofprosses = PRIME_PROCESS_COUNT
    while True:
        time.sleep(2)
        if numofprosses < 14:
            numofprosses += 1
            print(numofprosses)
            if Calculateifprime.qsize() > 1000:
                pool = mp.Process(target=prime_process, args=(Calculateifprime, primes))
                pool.start()
                PrimeProsseses.append(pool)
                Calculateifprime.put("NO_MORE_VALUES")
                print("addedprocess")
                print(numofprosses)
        else:
            print("Hit Limit")
            break
            



    # TODO wait for them to complete
    for p in PrimeProsseses:
        p.join()
    read.join()
    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()


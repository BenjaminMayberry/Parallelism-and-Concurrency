"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

Add any comments for me:



"""
from asyncio.windows_events import NULL
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import time

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2


def write(lock, semaphore, list_to_recive, shared_list, index_Write, release_limiter, Readerlocation, writer = 0):
  while Readerlocation.value <= list_to_recive:
    semaphore.acquire()
    lock.acquire()
    if Readerlocation.value > list_to_recive:
      lock.release()
      break
    index = index_Write.value % 10
    shared_list[index] = Readerlocation.value
    Readerlocation.value += 1
    index_Write.value += 1
    lock.release()
    release_limiter.release()
  if writer == 1:
    for i in range(2):
      # print("Done")
      semaphore.acquire()
      shared_list[(index_Write.value + i) % 10] = "END"
      release_limiter.release()

    # break
    # pass

def read(write_lock, semaphore, shared_list, index_Read, release_limiter):
  test = 0
  while True:
    
    write_lock.acquire()
    release_limiter.acquire()
    index = index_Read.value % 10
    # print(f"index {index_Read.value}")

    if shared_list[index] == "END":
      #print("done")
      write_lock.release()
      break
    else:
      test += 1
      index_Read.value += 1

    print(f"{shared_list[index]}")
    write_lock.release()
    semaphore.release()

    # break
    # semaphore.release()
    
def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000) # 3330
    
    smm = SharedMemoryManager()
    
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    sl = smm.ShareableList(range(BUFFER_SIZE))
    for f in range(BUFFER_SIZE):
      sl[f] = NULL
    Readerlocation = mp.RawValue('i', 1)
    Variables_Reader = mp.RawValue('i', 0)
    Variables_Write = mp.RawValue('i', 0)
    
    # Variables_Reader.value = 1
    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    read_lock = mp.Lock()
    write_lock = mp.Lock()
    circle_que_size = mp.Semaphore(BUFFER_SIZE)
    release_limiter = mp.Semaphore(0)
    prosseses = []
    # TODO - create reader and writer processes
    w1 = mp.Process(target=write, args=(read_lock, circle_que_size, items_to_send, sl, Variables_Write, release_limiter, Readerlocation, 1))
    prosseses.append(w1)

    r1 = mp.Process(target=read, args=(write_lock, circle_que_size, sl, Variables_Reader, release_limiter))
    prosseses.append(r1)


    for x in range(READERS - 1):
      r1 = mp.Process(target=write, args=(read_lock, circle_que_size, items_to_send, sl, Variables_Write, release_limiter, Readerlocation))
      prosseses.append(r1)

    for x in range(WRITERS  - 1):
      w1 = mp.Process(target=read, args=(write_lock, circle_que_size, sl, Variables_Reader, release_limiter))
      prosseses.append(w1)
    # TODO - Start the processes and wait for them to finish
    for i in prosseses:
      i.start()

    for i in prosseses:
      i.join()
      


    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    print(f'{Variables_Reader.value} values received')
    smm.shutdown()


if __name__ == '__main__':
    main()

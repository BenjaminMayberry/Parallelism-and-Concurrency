"""
Course: CSE 251, week 14
File: common.py
Author: <your name>

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')


You will lose 10% if you don't detail your part 1 
and part 2 code below

Describe how to speed up part 1

I made every recurcive call a thread to create as many threads as possible to do the api wait times


Describe how to speed up part 2

I made every function call a thread to reduce the call time


10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import multiprocessing as mp
import time


# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree):
    # TODO - implement Depth first retrieval
    
    # print('WARNING: DFS function not written')

    # Requesting a family from the server:
    if family_id:
        pass
    else:
        return

    

    family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    family.start()
    family.join()
    # print(family.response)
    tree.add_family(Family(family_id, family.response))

    husband = Request_thread(f'{TOP_API_URL}/person/{family.response["husband_id"]}')
    husband.start()
    husband.join()
    tree.add_person(Person(husband.response))
    
    wife = Request_thread(f'{TOP_API_URL}/person/{family.response["wife_id"]}')
    wife.start()
    wife.join()
    tree.add_person(Person(wife.response))
    

    husband_Thread = threading.Thread(target=depth_fs_pedigree, args=(husband.response["parent_id"], tree))
    husband_Thread.start()
    wife_Thread = threading.Thread(target=depth_fs_pedigree, args=(wife.response["parent_id"], tree))
    wife_Thread.start()


    test = family.response["children"]
    children = []
    for i in test:
        if tree.get_person(i):
            pass
        
        else:
            c = Request_thread(f'{TOP_API_URL}/person/{i}')
            
            children.append(c)
        
    for i in children:
        i.start()

    for i in children:
        i.join()
        tree.add_person(Person(i.response))
    
    
    husband_Thread.join()
    wife_Thread.join()


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    
    # FamilyURL, FamilyData = mp.Pipe()
    # PepoleURL, PepoleData = mp.Pipe()
    # FamilyURL.send(start_id)
    
    family = threading.Thread(target=Family_prosses, args=(start_id, tree))
    family.start()
    family.join()
    print("done")
    

def Family_prosses(Family_id, tree):
            familyID = Family_id
            # print(familyID)
            family = Request_thread(f'{TOP_API_URL}/family/{familyID}')
            family.start()
            family.join()
            test = Family(family.response["id"], family.response)
            tree.add_family(test)

            hs = threading.Thread(target=Person_prosses, args=(family.response["husband_id"], tree))
            hs.start()
            
            wf = threading.Thread(target=Person_prosses, args=(family.response["wife_id"], tree))
            wf.start()
            

            children = family.response["children"]
            test = []
            for i in children:
                c = Request_thread(f'{TOP_API_URL}/person/{i}')
                # print(f'{TOP_API_URL}/person/{i}')
                test.append(c)
        
            for i in test:
                i.start()

            for i in test:
                i.join()
                if tree.get_person(i.response['id']):
                    pass
                else:
                    tree.add_person(Person(i.response))
            hs.join()
            wf.join()

def Person_prosses(PepoleData, tree):
    person = PepoleData
    # print(person)
    personData = Request_thread(f'{TOP_API_URL}/person/{person}')
    personData.start()
    personData.join()
    if personData.response["parent_id"]:        
        per = threading.Thread(target=Family_prosses, args=(personData.response["parent_id"], tree))
        per.start()
        per.join()
        
        

    if tree.get_person(personData.response['id']):
        pass
    else:
        tree.add_person(Person(personData.response))





# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    print('WARNING: BFS (Limit of 5 threads) function not written')

    pass

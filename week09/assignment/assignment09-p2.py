"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

<Answer here>


Why would it work?

<Answer here>

"""
import math
import threading

from cv2 import dft 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color
# class solve_thread(threading.Thread):
#     def __init__(self, done, maze):
#         threading.Thread.__init__(self)
#         self.compleate = done
#         self.Maze = maze

#     def solve_find_end(row, col):
#         self.maze.move(row, col, COLOR)
#         if self.maze.at_end(row, col):
#             print("done")
#             # path.insert(0, [row,col])
#             return True
#         else:
#             # print(f"{row}{col}")
#             # time.sleep(1)
#             possible = maze.get_possible_moves(row, col)
#             # print(possible)
#             if len(possible) == 0:
#                 return False
#                 # print("No Possible Moves")
#             else:    
#                 for ro, co in possible:
#                     if maze.can_move_here(ro, co):
#                         # print(f"going to {ro} {co}")
#                         valid_move = recursive_path( ro, co)
#                         if valid_move:
#                             path.insert(0, [ro, co])
#                             return True
#                         else:
#                             maze.restore(ro, co)
#                     else: 
#                         return False
#     def run(self):
#         solve_find_end(self.row, self.col)
        

# def solve_find_end(maze):
#     """ finds the end position using threads.  Nothing is returned """
#     # When one of the threads finds the end position, stop all of them
# # TODO start add code here
#     x, y = maze.get_start_pos()
#     path = []
    
#     #recursive_path(maze, path, x, y)
    
#     def recursive_path(row, col):
#         #path.append([row, col])
#         maze.move(row, col, COLOR)
#         if maze.at_end(row, col):
#             print("done")
#             # path.insert(0, [row,col])
#             return True
#         else:
#             # print(f"{row}{col}")
#             # time.sleep(1)
#             possible = maze.get_possible_moves(row, col)
#             # print(possible)
#             if len(possible) == 0:
#                 return False
#                 # print("No Possible Moves")
#             else:    
#                 for ro, co in possible:
#                     valid_moves_that_can_be_done = []
#                     if maze.can_move_here(ro, co):
#                         valid_moves_that_can_be_done.append([ro, co])
#                         for rows, coloms in valid_moves_that_can_be_done:
#                             if valid_moves_that_can_be_done[0][0] == ro and valid_moves_that_can_be_done[0][1] == co:
#                                 valid_move = recursive_path( ro, co)
#                                 if valid_move:
#                                     path.insert(0, [ro, co])
#                                     return True
#                                 else:
#                                     maze.restore(ro, co)
#                             else: 
#                                 return False
#                                 # print("No Possible Moves")
#                     else:
#                         pass
                    
                    
#                     # print(possible[0])
#                     # print(f"row: {possible[0][0]} col: {possible[0][1]}")
                    


#                     # if possible[0][0] == ro and possible[0][1] == co:
#                     #     if maze.can_move_here(ro, co):
#                     #         # print(f"going to {ro} {co}")
#                     #         valid_move = recursive_path( ro, co)
#                     #         if valid_move:
#                     #             path.insert(0, [ro, co])
#                     #             return True
#                     #         else:
#                     #             maze.restore(ro, co)
#                     #     else: 
#                     #         return False
#                     #         # print("No Possible Moves")
#                     # else:
#                     #     if maze.can_move_here(ro, co):
#                     #         # print(f"going to {ro} {co}")
#                     #         valid_move = recursive_path( ro, co)
#                     #         if valid_move:
#                     #             path.insert(0, [ro, co])
#                     #             return True
#                     #         else:
#                     #             maze.restore(ro, co)
#                     #     else: 
#                     #         return False


#     pass
#     recursive_path(x,y)
#     path.insert(0, [x, y])

def solve_find_end(maze):
    x, y = maze.get_start_pos()
    global thread_count
    thread_count += 1
    #recursive_path(maze, path, x, y)
    finished = 1
    thread_lock = threading.Lock()

    def recursive_path(row, col, color, thread_lock):
        nonlocal finished
        nonlocal maze
        global thread_count
        if (finished) == 1:
            #path.append([row, col])


            thread_lock.acquire()
            
            if maze.can_move_here(row, col):
                maze.move(row, col, color)
            
            thread_lock.release()


            if maze.at_end(row, col):
                print("done")
                finished = 0
                # path.insert(0, [row,col])
                return True
            else:
                # print(f"{row}{col}")
                #time.sleep(1)
                possible = maze.get_possible_moves(row, col)
                possible_moves = []
                # thread.acquire()
                for ro, co in possible:
                    if maze.can_move_here(ro, co):
                        possible_moves.append([ro, co])
                
                #print(possible)
                if len(possible_moves) == 0:
                    return False
                    #print("No Possible Moves")
                else:    
                    for ro, co in possible_moves:
                        threads = []
                        if possible_moves[0][0] == ro and possible_moves[0][1] == co:
                            recursive_path( ro, co, color, thread_lock)

                            #ffprint(f"going to {ro} {co}")
                            # valid_move = recursive_path( ro, co, color)
                            # if valid_move:
                            #     return True
                            # else:
                            #     maze.restore(ro, co)
                        else: 
                            thread = threading.Thread(target=recursive_path, args=(ro, co, get_color(), thread_lock))
                            thread.start()
                            thread_count += 1
                        for i in threads:
                            i.join()

        else:
            return False    
    
    # print(get_color())                  
    recursive_path( x, y, get_color(), thread_lock)
    

    maze
    return



def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()
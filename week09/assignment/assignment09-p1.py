"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: <Add name here>

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# TODO add any functions
# def recursive_path(maze, path, row, col):
#     path.append([row, col])
#     if maze.at_end(path[-1][0], path[-1][1]):
#         print(path)
#         return[path]
#     else:
        
#         possible = maze.get_possible_moves(row, col)
#         if len(possible) == 0:
#             pass
#         else:    
#             for ro, co in possible:
#                 if maze.can_move_here(ro, co):
#                         recursive_path(maze, path, ro, co)
#     pass


    



def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
        
    # TODO start add code here
    x, y = maze.get_start_pos()
    path = []
    
    #recursive_path(maze, path, x, y)
    
    def recursive_path(row, col):
        #path.append([row, col])
        maze.move(row, col, COLOR)
        if maze.at_end(row, col):
            print("done")
            # path.insert(0, [row,col])
            return True
        else:
            # print(f"{row}{col}")
            #time.sleep(1)
            possible = maze.get_possible_moves(row, col)
            #print(possible)
            if len(possible) == 0:
                return False
                #print("No Possible Moves")
            else:    
                for ro, co in possible:
                    if maze.can_move_here(ro, co):
                        
                        #ffprint(f"going to {ro} {co}")
                        valid_move = recursive_path( ro, co)
                        if valid_move:
                            path.insert(0, [ro, co])
                            return True
                        else:
                            maze.restore(ro, co)
                    else: 
                        return False
                        #print("No Possible Moves")
    
                        
    recursive_path(x,y)
    path.insert(0, [x, y])
    # print(path)

    maze
    return path


def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()
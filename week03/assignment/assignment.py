"""
------------------------------------------------------------------------------
Course: CSE 251
Lesson Week: 03
File: assignment.py
Author: Benajmin Mayberry

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment

------------------------------------------------------------------------------
"""

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

# TODO Your final video need to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 300

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    #print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# TODO add any functions to need here
def designate_images(image_number):
    image_file = rf'elephant/image{image_number:03}.png'
    green_file = rf'green/image{image_number:03}.png'
    process_file = rf'processed/image{image_number:03}.png'
    
    create_new_frame(image_file, green_file, process_file)


if __name__ == '__main__':
    # single_file_processing(300)
    # print('cpu_count() =', cpu_count())
    all_process_times = timeit.default_timer()
    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []
    cpu = CPU_COUNT
    

    # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
    #      add results to xaxis_cpus and yaxis_times
    
    images = list(range(1, FRAME_COUNT + 1))

    # sample code: remove before submitting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # process one frame #10
    image_number = 10

    #image_file = rf'elephant/image{image_number:03d}.png'
    #green_file = rf'green/image{image_number:03d}.png'
    #process_file = rf'processed/image{image_number:03d}.png'

    #start_time = timeit.default_timer()
    #create_new_frame(image_file, green_file, process_file)
    #print(f'\nTime To Process all images = {timeit.default_timer() - start_time}')
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    
    
    for pr in range(1, cpu + 1):
      all_process_time = timeit.default_timer()
      xaxis_cpus.append(pr)
      with mp.Pool(pr) as p:
          p.map(designate_images, (images))
      log.write(f'Total Time for {cpu} CPU processing: {timeit.default_timer() - all_process_time}')
      yaxis_times.append(timeit.default_timer() - all_process_time)
      print(f"{pr} cpu finished")


    log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_times}')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()

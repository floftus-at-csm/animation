from PIL import ImageFile, Image, ImageFilter
import numpy as np
import inspect
from os import path, listdir
ImageFile.LOAD_TRUNCATED_IMAGES = True # used to stop errors with file size
import subprocess
import sys
from os import listdir, makedirs
from os.path import isfile, join, dirname
from skimage import io, util
from skimage.util import compare_images
from skimage.color import rgb2gray
import argparse
import random
from helper_functions import create_frames_for_masks, list_relative_paths_in_directory, merge_frames_into_videos
import skvideo.io
import skvideo.datasets

# 1. use ffmpeg-python to save video as numpy array - potentially just use scikit-video?
# 2. process it line by line and shift pixels into the next frame
# 3. I might need to create a new array to do this and paste image in 



# =========================================================================
# e.g. python3 compositing_multiple_views.py content/oct24/original/tree_angles_straight content/oct24/frames/tree_angles_straight/ content/oct24/processed/tree_angles_straight/
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input")
    parser.add_argument("--fps", help="set fps for splitting frame", default = "25")
    parser.add_argument("--output", help="set name of output folder")
    parser.add_argument("--process", default="composite")
    parser.add_argument("--shuffle", default="False")
    args=parser.parse_args()

    videodata = skvideo.io.vread(args.input)
    print(videodata.shape)
    # print(videodata[0][0][0]) # gets you top left pixel from frame one
    # print(videodata[0][1][0]) # gets one pixel to the right of top left pixel
    # print(videodata[0][x]) # gets all the horizontal pixel strips
    # print(videodata[a]) # gets you the individual frames

    new_video = np.empty_like(videodata)
    print("new video shape is: ", new_video.shape)
    # new_video2 = np.empty_like(videodata)
    count = 0
    for i in range (0, 384-1):
        for j in range(0, 1080-1):
            new_video[i][j] = videodata[count][j] # so this then cycling through the  frames vertically - there would be about 3 time zones
            if j % 20 == 0:
            # if i % 5 == 0:
                if(count < 383):
                    count = count + 1
                else:
                    count = 0

    skvideo.io.vwrite("outputvideo_modulo3.mp4", new_video)
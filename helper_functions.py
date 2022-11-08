
from PIL import ImageFile, Image
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

def load_images_in_folder(path):
    # return array of images

    imagesList = listdir(path)
    loadedImages = []
    for image in imagesList:
        img = Image.open(path + image)
        loadedImages.append(img)
        return loadedImages

def list_files_in_directory(path_to_directory):
    onlyfiles = [f for f in listdir(path_to_directory) if isfile(join(path_to_directory, f))]
    # I'm not sure why but the join is not working
    onlyfiles = sorted(onlyfiles)
    return onlyfiles

def list_relative_paths_in_directory(path_to_directory, shuffle_v):
    onlyfiles = [join(path_to_directory + f) for f in listdir(path_to_directory) if isfile(join(path_to_directory, f))]
    # I'm not sure why but the join is not working
    if(shuffle_v == "True"):
        random.shuffle(onlyfiles)
        print("shuffle v is true")
    else:
        onlyfiles = sorted(onlyfiles)
    print(onlyfiles)
    return onlyfiles

def safe_open_w(path):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    makedirs(dirname(path), exist_ok=True)
    return open(path, 'w')

def load_image(path):
    img = Image.open(path)
    return img

def split_video_to_images(video_path, output_location, fps_value):
    # os.system or subprocess
    # potential to not use every frame
    final_loc = output_location + "/%09d.png"
    fps_string = "fps="+fps_value
    subprocess.run(["ffmpeg", "-i", video_path, "-vf", fps_string, final_loc])
    # load_image()output_location + "/0000001.png"
    # !ffmpeg -i test.mp4 /content/frames/test-%09d.png

def get_frames_from_directories(location_of_frames, num_videos, shuffle_val):
    the_frames = [None] * num_videos
    for i in range(0, num_videos):
        the_frames[i] = list_relative_paths_in_directory(location_of_frames  + str(i) + "/", shuffle_val)
    max_frames = len(max(the_frames))
    num_frames_overall = 0
    for i in range(0, len(the_frames)):
        num_frames_overall = num_frames_overall + len(the_frames[i])
    print("the current frames are: ", the_frames)
    print("the number of overall frames are: ", num_frames_overall)
    return the_frames, max_frames, num_frames_overall

def merge_frames_into_videos(frame_path, video_name):
    frame_arg = frame_path + "/%06d.png"
    video_path = frame_path + "/" + video_name
    subprocess.run(["ffmpeg", "-i", frame_arg, "-r", "24", video_name])

def create_frames_for_masks(video_paths, output_location, fps_val):
    makedirs(dirname(output_location), exist_ok=True) # create folder for output frames if it doesn't exist
    # for all the video paths create a directory for their frames and then split the videos into those folders
    # for count, value in enumerate(video_paths):
    full_output_loc = output_location + "/mask/"
    makedirs(dirname(full_output_loc), exist_ok=True)
    full_output_loc = output_location + "/to_mask/"
    makedirs(dirname(full_output_loc), exist_ok=True)
    split_video_to_images(video_paths[0], output_location + "/mask", fps_val)
    split_video_to_images(video_paths[1], output_location + "/to_mask", fps_val)


def merge_frames_into_videos(frame_path, video_name, framerate):
    frame_arg = frame_path + "/%06d.png"
    video_path = frame_path + "/" + video_name
    subprocess.run(["ffmpeg", "-i", frame_arg, "-r", framerate, video_name])
    # !ffmpeg -i /content/frames/test-%09d.png -r 60 test-merged.mp4
# 
# python compositing_multiple_views.py <video_location
# 

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

def create_frames(path_to_videos, video_paths, output_location, fps_val):
    makedirs(dirname(output_location), exist_ok=True) # create folder for output frames if it doesn't exist
    # for all the video paths create a directory for their frames and then split the videos into those folders
    for count, value in enumerate(video_paths):
        full_output_loc = output_location + "/" + str(count) + "/"
        print(full_output_loc)
        makedirs(dirname(full_output_loc), exist_ok=True)
        split_video_to_images(path_to_videos + "/" + value, output_location + "/" + str(count), fps_val)

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

def reorder_frames(frames, order, num_videos, max_frames):
    new_order_for_frames = []
    if(order == "simple"):
        for i in range(0, max_frames):
            for j in range(0, num_videos):
                try:
                    new_order_for_frames.append(frames[j][i])
                    print(len(new_order_for_frames))
                except:
                    print("this frame doesn't exist: ")
                    print("i = ", i)
                    print("j = ", j)
        # print(new_order_for_frames)
        print("the new frame order is: ", new_order_for_frames)
        return new_order_for_frames

def merge_frames_into_videos(frame_path, video_name):
    frame_arg = frame_path + "/%06d.png"
    video_path = frame_path + "/" + video_name
    subprocess.run(["ffmpeg", "-i", frame_arg, "-r", "24", video_name])
    # !ffmpeg -i /content/frames/test-%09d.png -r 60 test-merged.mp4

def process_individual_frames(frame_order, process):
    output_frame_value = 0
    for count, value in enumerate(frame_order[:-1]):
        if(process == "difference"):
            image1 = io.imread(frame_order[count])
            image2 = io.imread(frame_order[count+1])
            image1_g = rgb2gray(image1)
            image2_g = rgb2gray(image2)
            differenced_image = compare_images(image1, image2, method='diff') # difference images
            # or remove background and then do processing
            file_num = str(output_frame_value).zfill(6)
            io.imsave(processed_loc + str(file_num) + ".png", differenced_image) # save image
        elif(process == "composite"):
            image1 = Image.open(frame_order[count]).convert('L')
            mask = Image.open(frame_order[count+1]).convert('L')
            if(count == 0):
                # potential to change this to modulo so it resets every so often - or a map!
                image2 = Image.open(frame_order[count+2]).convert('L')
            else:
                image2 = composite
            composite = Image.composite(image1, image2, mask)
            # rename files - equivalent of this  #  num=0; for i in *; do mv "$i" "$(printf '%09d' $num).${i#*.}"; ((num++)); done
            file_num = str(output_frame_value).zfill(6)
            composite.save(processed_loc + str(file_num) + ".png") # save image
        elif(process == "comp_diff"):
            image1 = io.imread(frame_order[count])
            image2 = io.imread(frame_order[count+1])
            image3 = io.imread(frame_order[count+1])
            image1_g = rgb2gray(image1)
            image2_g = rgb2gray(image2)
            image3_g = rgb2gray(image2)
            differenced_image = compare_images(image1, image2, method='diff') # difference images
            differenced_image2 = compare_images(image2, image3, method='diff') # difference images
            pil_im1 = Image.fromarray(util.img_as_ubyte(differenced_image)).convert('L')
            pil_im2 = Image.fromarray(util.img_as_ubyte(differenced_image2)).convert('L')
            mask = Image.fromarray(util.img_as_ubyte(image1)).convert('L')
            composite = Image.composite(pil_im1, pil_im2, mask)
            file_num = str(output_frame_value).zfill(6)
            composite.save(processed_loc + str(file_num) + ".png") # save image
        elif(process == "comp_diff2"):
            image1 = io.imread(frame_order[count])
            image2 = io.imread(frame_order[count+1])
            image3 = io.imread(frame_order[count+1])
            image1_g = rgb2gray(image1)
            image2_g = rgb2gray(image2)
            image3_g = rgb2gray(image2)
            differenced_image = compare_images(image1, image2, method='diff') # difference images
            differenced_image2 = compare_images(image1, image3, method='diff') # difference images
            pil_im1 = Image.fromarray(util.img_as_ubyte(differenced_image)).convert('L')
            pil_im2 = Image.fromarray(util.img_as_ubyte(differenced_image2)).convert('L')
            mask = Image.fromarray(util.img_as_ubyte(image1)).convert('L')
            if(count == 0):
                composite = Image.composite(pil_im1, pil_im2, mask)
            else:
                composite = Image.composite(pil_im1, composite, pil_im2)
            file_num = str(output_frame_value).zfill(6)
            composite.save(processed_loc + str(file_num) + ".png") # save image
        output_frame_value = output_frame_value + 1

# def grayscale_process():
#     # code goes here

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

    path_to_videos = args.input
    output_loc = path_to_videos.replace("/original/", "/frames/")
    the_videos = list_files_in_directory("path_to_videos") # get the file paths of videos in the folder provided - folder needs to only have videos in it
    number_of_videos = len(the_videos)
    frame_loc = output_loc
    processed_loc = path_to_videos.replace("/original/", "/processed/")
    if(args.output != None):
        processed_loc = processed_loc + args.output + "/"

    print(the_videos)
    print(output_loc)
    
    # create_frames(path_to_videos, the_videos, output_loc, args.fps)

    # # ##################
    current_frames, max_frame_num, overall_frame_num = get_frames_from_directories(frame_loc, number_of_videos, args.shuffle) # get frames from directories
    # new_frame_order_v = reorder_frames(current_frames, "simple", number_of_videos, max_frame_num)
    # makedirs(dirname(processed_loc), exist_ok=True) # create folder for output frames
    # process_individual_frames(new_frame_order_v, args.process)  # loop over new frame order and 

    # merge_frames_into_videos(processed_loc, "blended_new_straight.mp4")

    # ffmpeg -i faces.mp4 -filter:v "setpts=40*PTS,minterpolate='fps=25:scd=none:me_mode=bidir:vsbmc=1:search_param=400'" -y search_param_400.mp4


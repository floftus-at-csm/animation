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


# 1. mask with another film - slow framerate + interpolate between frames
# 2. silhouette a film with a mask (output is dark black on top of film)
# 3. use text as a mask - play with different fonts combine with 

def process_simple(path_to_mask, path_to_image, blur_level, threshold = 125):
    starter_mask = Image.open(path_to_mask)
    red, green, blue = starter_mask.split()
    threshold = blue.point(lambda x: 255 if x > threshold else 0)
    # threshold = threshold.convert("1")
    mask_blur = threshold.filter(ImageFilter.GaussianBlur(blur_level))
    image = Image.open(path_to_image)
    im = Image.composite(image, mask_blur, mask_blur)
    return im

def process_simple_color(path_to_mask, path_to_image, blur_level, threshold = 125):
    starter_mask = Image.open(path_to_mask)
    red, green, blue = starter_mask.split()
    threshold = blue.point(lambda x: 255 if x > threshold else 0)
    # threshold = threshold.convert("1")
    mask_blur = threshold.filter(ImageFilter.GaussianBlur(blur_level))
    image = Image.open(path_to_image)
    rgbimg = Image.new("RGBA", mask_blur.size)
    rgbimg.paste(mask_blur)
    im = Image.composite(image, rgbimg, mask_blur)
    return im

# =========================================================================
# e.g. python3 compositing_multiple_views.py content/oct24/original/tree_angles_straight content/oct24/frames/tree_angles_straight/ content/oct24/processed/tree_angles_straight/
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mask")
    parser.add_argument("--input")
    parser.add_argument("--fps", help="set fps for splitting frame", default = "25")
    parser.add_argument("--output", help="set name of output folder")
    parser.add_argument("--process", default="composite")
    parser.add_argument("--shuffle", default="False")
    args=parser.parse_args()

    path_to_mask = args.mask
    path_to_video = args.input
    the_videos = [path_to_mask, path_to_video]
    output_loc = "content/oct24/processed/masking/" + args.output
    # create_frames_for_masks(the_videos, output_loc, args.fps)

    mask_paths = list_relative_paths_in_directory(output_loc + '/mask/', args.shuffle)
    # print(mask_paths)
    to_mask_paths = list_relative_paths_in_directory(output_loc + '/to_mask/', args.shuffle)
    print(mask_paths)
    for count, value in enumerate(mask_paths[0:300]):
    #     # if(count % 5 == 0){
    #     #     change mask
    #     # }
        processed = process_simple_color(value, to_mask_paths[count],  10, 100) # try using sin to vary the threshold
        file_num = str(count).zfill(6)
        processed.save(output_loc + "/" +str(file_num) + ".png") # save image
    framerate = "8"    
    merge_frames_into_videos(output_loc, args.output + ".mp4", framerate)

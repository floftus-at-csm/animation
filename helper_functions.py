
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
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



# 1. mask with another film - slow framerate + interpolate between frames
# 2. silhouette a film with a mask (output is dark black on top of film)
# 3. use text as a mask - play with different fonts combine with 
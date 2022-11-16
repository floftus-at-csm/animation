
from helper_functions import list_files_in_directory
from skimage import io, filters
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from skimage.util import compare_images
import numpy as np
from skimage import exposure

def grayscale_image(im):
    im1 = rgb2gray(im)
    return im1

# def difference(im1, im2):
#     diff_rotated = compare_images(im1, im2, method='diff')
#     return diff_rotated

def hysteris_threshold(image1, low = 0.0075, high = 0.05, output_path="default", save=True):
    edges = filters.sobel(image1)
    print("done edge detection")
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig = plt.figure(frameon=False)
    fig.set_size_inches(18.5 , 10.5)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    lowt = (edges > low).astype(int)
    hight = (edges > high).astype(int)
    hyst = filters.apply_hysteresis_threshold(edges, low, high)  
    ax.imshow(hight + hyst, cmap='magma')
    fig.set_size_inches(17.5, 10.5)

    fig.savefig(output_path, dpi=100)

# from skimage.viewer import ImageViewer
# load all the frames

# split them into groups based on time: 6 x 8 = 48

# for each group do edge detection for each frame

# then do Hysteresis thresholding 

# try to combine together images

# also export frames as a video
image_paths = list_files_in_directory('content/Rachy/frames')
print('content/Rachy/frames/' + image_paths[0])
starter_image = io.imread('content/Rachy/frames/' + image_paths[0])
starter_grayscale = grayscale_image(starter_image)
p2, p98 = np.percentile(starter_grayscale, (2, 98))
initial_rescale = exposure.rescale_intensity(starter_grayscale, in_range=(p2, p98))
# for count, value in enumerate(image_paths):
for i in range(1, int(len(image_paths)/30)):
    image_to_compare = io.imread('content/Rachy/frames/' + image_paths[i*30])
    comparison_grayscale = grayscale_image(image_to_compare)
    p2, p98 = np.percentile(comparison_grayscale, (2, 98))
    img_rescale = exposure.rescale_intensity(comparison_grayscale, in_range=(p2, p98))
    diff_im = compare_images(img_rescale, initial_rescale, method='diff')
    path_v = "content/Rachy/new_test/" + str(i) + ".png"
    hysteris_threshold(diff_im, 0.02, 0.09, path_v) # 0.02 and 0.09 is good






  


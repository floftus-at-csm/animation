
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
    ax.imshow(hight + hyst, cmap='plasma')
    fig.set_size_inches(17.5, 10.5)
    return fig
    # fig.savefig(output_path, dpi=300)

def prep_group(i, num, paths):
    current_image = i
    for j in range(0, num):
        image_to_compare = io.imread('content/Rachy/frames/' + image_paths[current_image])
        if j == 0:
            image_to_compare2 = io.imread('content/Rachy/frames/' + image_paths[current_image+1])
        else:
            image_to_compare2 = comparison
        comparison = compare_images(image_to_compare, image_to_compare2, method='blend')
    comparison = grayscale_image(comparison)
    return comparison
        # p2, p98 = np.percentile(comparison_grayscale, (2, 98))

def just_hystersis(image1, low = 0.0075, high = 0.05):
    edges = filters.sobel(image1)
    lowt = (edges > low).astype(int)
    hight = (edges > high).astype(int)
    hyst = filters.apply_hysteresis_threshold(edges, low, high)  
    return hyst, hight

def just_hystersis_with_blended(image1, image2, low = 0.0075, high = 0.05):
    # meijering, sato, frangi, hessian
    edges = filters.sobel(image1)
    edges2 = filters.sobel(image2)
    lowt = (edges > low).astype(int)
    hight = (edges2 > high).astype(int)
    hyst = filters.apply_hysteresis_threshold(edges, low, high)  
    return hyst, hight

def create_figure_and_save(output_path, image_hight, image_hyst, color_mode):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig = plt.figure(frameon=False)
    fig.set_size_inches(18.5 , 10.5)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(image_hight + image_hyst, cmap=color_mode)
    fig.set_size_inches(17.5, 10.5)
    fig.savefig(output_path, dpi=100)

# from skimage.viewer import ImageViewer
# load all the frames

# split them into groups based on time: 6 x 8 = 48

# for each group do edge detection for each frame

# then do Hysteresis thresholding 

# try to combine together images

# also export frames as a video
image_paths = list_files_in_directory('content/Rachy/circadian/frames')
print('content/Rachy/frames/' + image_paths[0])
starter_image = io.imread('content/Rachy/circadian/frames/' + image_paths[0])
starter_grayscale = grayscale_image(starter_image)
p2, p98 = np.percentile(starter_grayscale, (2, 98))
initial_rescale = exposure.rescale_intensity(starter_grayscale, in_range=(p2, p98))

for i in range(1, int(len(image_paths))):
    image_to_compare = io.imread('content/Rachy/circadian/frames/' + image_paths[i])
    comparison_grayscale = grayscale_image(image_to_compare)
    p2, p98 = np.percentile(comparison_grayscale, (2, 98))
    img_rescale = exposure.rescale_intensity(comparison_grayscale, in_range=(p2, p98))
    diff_im = compare_images(img_rescale, initial_rescale, method='diff')
    path_v = "content/Rachy/circadian/output5/" + str(i) + ".png"
    the_fig, image_hight = just_hystersis(diff_im, 0.005, 0.07) # originally 0.02 and 0.09
    
    if(i==1):
        # the_fig, image_hight = just_hystersis_with_blended(diff_im, diff_im, 0.02, 0.09)
        blended = compare_images(the_fig, starter_grayscale, method='blend')
        
    else:
        # the_fig, image_hight = just_hystersis_with_blended(diff_im, blended, 0.02, 0.09)
        blended = compare_images(the_fig, blended, method='blend')
    if(i % 30 == 0):
        create_figure_and_save(path_v, image_hight, blended, 'plasma')
        # the_fig.savefig(path_v, dpi=300)





  




  



from helper_functions import list_files_in_directory
from skimage import io, filters
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from skimage.util import compare_images

def hysteris_threshold(image1, low = 0.0075, high = 0.05, save=True):
    im1 = rgb2gray(image1)
    edges = filters.sobel(im1)
    print("done edge detection")
    fig, ax = plt.subplots(nrows=1, ncols=1)
# from skimage.viewer import ImageViewer
# load all the frames

# split them into groups based on time: 6 x 8 = 48

# for each group do edge detection for each frame

# then do Hysteresis thresholding 

# try to combine together images

# also export frames as a video
image_paths = list_files_in_directory('content/Rachy/frames')
starter_image = io.imread(image_paths[0])

# image_color = io.imread("content/Rachy/00001.png")
# image_color2 = io.imread("content/Rachy/00301.png")
# image = rgb2gray(image_color)
# image2 = rgb2gray(image_color2)
# edges = filters.sobel(image)
# edges2 = filters.sobel(image2)
# print("done edge detection")
# low = 0.0075
# high = 0.05
# fig, ax = plt.subplots(nrows=1, ncols=1)

fig = plt.figure(frameon=False)
fig.set_size_inches(18.5 , 10.5)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)

lowt = (edges > low).astype(int)
hight = (edges > high).astype(int)
hyst = filters.apply_hysteresis_threshold(edges, low, high)   

ax.imshow(hight + hyst, cmap='magma')
fig.set_size_inches(18.5, 10.5)

fig.savefig('content/rachy/hyst_matplotliba.png', dpi=300)
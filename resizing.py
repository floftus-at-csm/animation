from PIL import Image

def standard_resize(image, scale):
    width, height = image.size
    newsize = (width * scale, height * scale)
    im1 = image.resize(newsize)
    return im1


def resize_folder(image_list, output_loc, scale):
    for count, image_path in enumerate(image_list):
        im = Image.open(image_path)
        resized = standard_resize(im, scale)
        resized.save(output_loc + str(count)+ ".png")
        

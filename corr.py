# doesn't account for shifts, assumes same size and shape
# it might output only until 1 for the zero norm per pixel (divided by file size)

import sys

from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

# makes everything into greyscale
def rgb_to_grey(image):
    if len(image.shape) ==3:
        return average(image, -1)
    else:
        return image

# normalizes images/changes them to the same mathematical reference fram
def normalize(image):
    valueRange = image.max() - image.min()
    return (image-image.min())*1/valueRange

# compares images
def compare_images(image1orig, image2orig):
    image1 = rgb_to_grey(image1orig)
    image2 = rgb_to_grey(image2orig)
    image1norm = normalize(image1)
    image2norm = normalize(image2)
    diff = image1norm - image2norm
    man_norm = sub(abs(diff))
    zero_norm = norm(diff.ravel(), 0)
    return (man_norm, zero_norm)

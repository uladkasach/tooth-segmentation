## this script defines functionality for loading raw images and label images in an interpertable format
## for our purposes, we can return each pixel in a one dimensional array. We are not concerned with spacial correlation. i.e., "unwrap" each image
## however, we should include the "wrap" functionality for each image. (that way we can displace each image as the block image rather than a concatenated line for demo)
from PIL import Image;
import numpy as np;
import matplotlib.pyplot as plt

'''
pix = im.load()
print im.size #Get the width and hight of the image for iterating over
print pix[5,5] #Get the RGBA Value of the a pixel of an image
print type(pix);
image = np.asarray(im);
print image.shape
print image.shape[0] * image.shape[1];
image = image.reshape(im.size[0] * im.size[1], 3);
print image.shape;
image = image.reshape(im.size[0], im.size[1], 3);
print image.shape;
## im = PIL.Image.fromarray(numpy.uint8(I))
'''

def unravel(image, size):
    return image.reshape(size[0] * size[1], 3);

def reravel(image, size, final_dim=3):
    return image.reshape(size[1], size[0], final_dim);

def load(src): ## returns [image, size]
    im = Image.open(src); ## e.g., "source/camel_1.jpg"
    return np.asarray(im), im.size;

def save(image, path):
    if(True):
        modified_im = Image.fromarray(image);
        modified_im.save(path) ## e.g., "out/test.bmp"
    else:
        plt.imshow(image) #Needs to be in row,col order
        plt.savefig(path)

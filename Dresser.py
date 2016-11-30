import sys
import getopt
import qrcode
# from skimage import transform,data
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:s:", ["help=", "image=", "sentence="])
    except getopt.GetoptError:
        print 'Please type in the image url and sentence -i <image> -s <sentence>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Dresser.py -i <image> -s <sentence>'
            sys.exit()
        elif opt in ("-i", "--image"):
            img_dress = np.array(Image.open(arg))
        elif opt in ("-s", "--sentence"):
            s = arg

    qr = qrinit(s)
    
    img = qr.make_image()
    img_array = np.array(img)
    img.save('QRCode.png', 'PNG')


    shape = img_array.shape
    print shape
    print img_dress.shape
    if(shape[0] > img_dress.shape[0] or shape[1] > img_dress.shape[1]):
        print 'error: image size not agree!'
        sys.exit(-1)
    mask = img_dress[:, :, 0] > 0.5
    mask = reduce(mask, shape)
    print mask.dtype
    print mask.shape
    scipy.misc.imsave('Mask.png', mask)
    mask_mask = np.random.randn(shape[0] * shape[1]).reshape((shape[0], shape[1]))
    mask_mask = mask_mask > 0
    mask *= mask_mask
    scipy.misc.imsave('Mask_masked.png', mask)
    img_array *= mask
    #img_produced = Image.fromarray(img_array.astype('uint8')*255)
    #img_produced.save('Result.png', 'PNG')
    scipy.misc.imsave('Result.png', img_array)   

def qrinit(s):
    qr = qrcode.QRCode(
	    version=None,
	    error_correction=qrcode.constants.ERROR_CORRECT_H,
	    box_size=10,
	    border=1,
    )
    qr.add_data(s)
    qr.make(fit=True)
    return qr

def reduce(image, shape):
    H = shape[0]
    W = shape[1]
    HH = image.shape[0]
    WW = image.shape[1]
    Hprop = int(HH / H)
    Wprop = int(WW / H)
    image_reduced = np.zeros(shape, dtype = bool)
    for i in range(H):
        for j in range(W):
            image_reduced[i,j] = image[i*Hprop,j*Wprop]
    return image_reduced

if __name__ == "__main__":
    main(sys.argv[1:])

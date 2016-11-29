import sys
import getopt
import qrcode
# from skimage import transform,data
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:s:", ["help=", "image=", "sentence="])
    except getopt.GetoptError:
        print('Please type in the image url and sentence -i <image> -s <sentence>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Dresser.py -i <image> -s <sentence>')
            sys.exit()
        elif opt in ("-i", "--image"):
            img_dress = np.array(Image.open(arg))
        elif opt in ("-s", "--sentence"):
        	s = arg

    qr = qrinit(s)
    
    img = qr.make_image()
    img_array = np.array(img)
    shape = img_array.shape
    print(img_array.dtype)
    print(shape)
    print(img_dress.shape)
    if(shape[0] > img_dress.shape[0] or shape[1] > img_dress.shape[1]):
        print('error: image size not agree!')
        sys.exit(-1)
    img_dress = img_dress[:, :, 0]
    img_dress[img_dress <= 127] = 0
    img_dress[img_dress > 127] = 1
    img_dress = reduce(img_dress, shape)

    img_produced = img_array * img_dress
    img_produced[img_produced == 1] = True
    img_produced[img_produced == 0] = False
    print(img_produced.shape)
    plt.imshow(img_produced)
    plt.axis('off')
    plt.show()

def qrinit(s):
    qr = qrcode.QRCode(
	    version=None,
	    error_correction=qrcode.constants.ERROR_CORRECT_H,
	    box_size=10,
	    border=4,
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
    image_reduced = np.zeros(shape)
    for i in range(H):
        for j in range(W):
            image_reduced[i,j] = image[i*Hprop,j*Wprop]
    return image_reduced

if __name__ == "__main__":
    main(sys.argv[1:])
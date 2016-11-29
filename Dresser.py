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

    img_dress = img_dress[:, :, 0]
    img_dress[img_dress <= 127] = 0 
    img_dress[img_dress > 127] = 1
    plt.imshow(img_dress)
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

# def Reduce(image,m,n):
#     H = int(image.height*m)
#     W = int(image.width*n)
#     size = (W,H)
#     image_reduced = cv.CreateImage(size,image.depth,image.nChannels)
#     for i in range(H):
#         for j in range(W):
#             x = int(i/m)
#             y = int(j/n)
#             image_reduced[i,j] = image[x,y]
#     return image_reduced

if __name__ == "__main__":
    main(sys.argv[1:])
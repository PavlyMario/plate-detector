import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage import io
from skimage.color import label2rgb
from PIL import Image 
import PIL


def plate_enhancement(img):
    mycolors = np.array([[0 ,0, 255],
             [0 ,255, 0],
             [0 ,255, 50],
             [0 ,255 ,150],
             [0 ,255, 200],
             [0 ,255 ,255],
             [100, 255, 100],
             [255 ,255 ,100],
             [255 ,255, 0],
             [255 ,255 ,200],
             [255 ,0, 150],
             [255 ,0 ,150],
             [255 ,80, 0],
             [255, 70, 0],
             [255 ,60 ,0],
             [255 ,80, 0],
             [255 ,90 ,0],
             [255 ,100, 0],
             [255 ,110 ,0],
             [255 ,120, 0],
             [255 ,130, 0],
             [255 ,140 ,0],
             [255 ,150 ,0],
             [255 ,160, 0],
             [255 ,170 ,0],
             [255 ,180 ,0],
             [255 ,190 ,0],
             [255 ,200 ,0],
             [255 ,210, 0],
             [255 ,220 ,0],
             [255 ,230, 0],
             [255 ,240 ,0]])/255
    
    # Convert to gray scale and B&W
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_img = cv2.threshold(grayImage,180 , 255, cv2.THRESH_BINARY_INV)[1]


    #Label and color plate img
    _,lbl_img,_, _=cv2.connectedComponentsWithStats(np.uint8(binary_img), 4, cv2.CV_32S)
    rgb_lbl_img = label2rgb(lbl_img,colors=mycolors,bg_label=1,bg_color=(255,255,255))
    
    #Remove border have RGB = [0,0,255]
    row, col = np.shape(binary_img)
    for r in range(0, row):
        for c in range(0, col):
            if rgb_lbl_img[r,c,2]==255:
                lbl_img[r,c] = 0

    #Remove remaining pixel from top part
    for r in range(1,int(row/3)):
        for c in range(1,col):
            if lbl_img[r,c] != 0:
                lbl_img[r,c] = 0

    #final image B&W
    final_img = cv2.threshold( np.uint8(lbl_img),0 , 255, cv2.THRESH_BINARY)[1]
    kernel1 =cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,5))
    final_img1 = cv2.dilate(final_img,kernel1,iterations = 1)
    #final_img1 = cv2.erode(final_img1,kernel1,iterations = 1)

    num_objects,_,dims,centers=cv2.connectedComponentsWithStats(np.uint8(final_img1), 4, cv2.CV_32S)
    plt.imshow(final_img,'gray')
    plt.show()
    plt.imshow(final_img1,'gray')
    plt.show()

    return final_img,num_objects,dims,centers,final_img1

# img = mpimg.imread(r'C:\Users\salah\OneDrive\Desktop\Image Project\image 3.jpg')
# binary_img,grayImage,lbl_img ,rgb_lbl_img,final_img,num_objects,centers=plate_enhancement(img)
# io.imshow(img)
# plt.show()
# io.imshow(grayImage)
# plt.show()
# io.imshow(binary_img)
# plt.show()
# io.imshow(rgb_lbl_img)
# plt.show()
#plt.imshow(final_img1,'gray')
# plt.savefig('final_img.png')
# plt.show()
# print(num_objects)
# print(centers)
#cv2.imwrite('final_img.jpg', final_img)




import cv2
import numpy as np
import sys
sys.setrecursionlimit(200000)
# author Yichen Wang

img = cv2.imread("/Users/saber/Desktop/Project_yichen/t3.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#convert to grayscale

'''
This is a function to split image into 4 images
the sub_image is based on original gray image.
   y1      y       y2
   |               |
x1-|-------|-------|
  -|   1   |   2   |
x -|-------|-------| 
  -|   3   |   4   |
x2-|-------|-------|
In this function it does not return the image, but return the new x1,x2,y1,y2 of sub_image

'''
def split(x1,x2,y1,y2):
    subs = [] #list of 4 sub_image
    x=(x1+x2)/2
    y=(y1+y2)/2
    sub_1 = [x1,x,y1,y]
    sub_2 = [x1,x,y,y2]
    sub_3 = [x,x2,y1,y]
    sub_4 = [x,x2,y,y2]
    subs.append(sub_1)
    subs.append(sub_2)
    subs.append(sub_3)
    subs.append(sub_4)

    return subs


'''
This is a function convert a list of [x1,x2,y1,y2] to image based on gray.
'''
def convert(l):
    x1 = l[0]
    x2 = l[1]
    y1 = l[2]
    y2 = l[3]
    image = gray[x1:x2,y1:y2]
    return image


'''
This is a function return mean and error of an image
'''
def mean_error(image):
    h,w = image.shape
    mean = np.mean(image)
    error = 0
    for i in range (h):
        for j in range (w):
            error += abs(image[i][j]-mean)
    return mean, error



'''
Quadtree function
imglist = a list of list([x1,x2,y1,y2])
errlist = a list of error, same order with imglist. save time in caluclate error
'''
def quadTree(x1,x2,y1,y2,imglist,errlist,meanlist):
    if (x2-x1)>1:#subimage size
        new4 = split(x1,x2,y1,y2)# new4 means new 4 subimages, it is a list of list
        for xyimg in new4:#xyimg is a list [x1,x2,y1,y2]
            imglist.append(xyimg)
            img = convert(xyimg)#convert to image
            m,e = mean_error(img)
            errlist.append(e)
            meanlist.append(m)
        #after add new 4 subimage into imglist and errlist. find the max err, remove the image with max err from both imglist and errlist
        maxe=max(errlist)

        #print (count)
        #print(" max error=",maxe)
        i = errlist.index(maxe)
        new_x1 = imglist[i][0]
        new_x2 = imglist[i][1]
        new_y1 = imglist[i][2]
        new_y2 = imglist[i][3]
        imglist = imglist[:i] + imglist[i + 1:]
        errlist = errlist[:i] + errlist[i + 1:]
        meanlist = meanlist[:i] + meanlist[i + 1:]
        quadTree(new_x1,new_x2,new_y1,new_y2,imglist,errlist,meanlist)
    else:# all pixels in same subimage should equals to mean, At first need to put the [x1,x2,y1,y2] back
        xyimg = [x1,x2,y1,y2]
        img = convert(xyimg)
        imglist.append(xyimg)
        m,e = mean_error(img)
        errlist.append(e)
        meanlist.append(m)
        #then set all imgs in imglist
        for i,mm in zip(imglist,meanlist):
            for i_h in range (i[0],i[1]):
                for i_w in range (i[2],i[3]):
                    gray[i_h][i_w] = mm




imglist = []
errlist = []
meanlist = []

h,w = gray.shape
quadTree(0,h,0,w,imglist,errlist,meanlist)



cv2.imshow("P2_image",gray)

cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np
# author Yichen Wang

img = cv2.imread("/Users/saber/Desktop/Project_yichen/t1.jpg")

'''
change image type from ndarray to list
'''
def tolist(i):
    l=[]
    for row in i:
        for pixel in row:
            l.append(pixel)
    return l

'''
Find which channel R,G,B has the greatest range in list
0-R, 1-G, 2-B
'''
def maxrange(l):
    rgb=[]
    maxr = max(l,key=lambda x:x[0])
    minr = min(l,key=lambda x:x[0])
    ranger = maxr[0] - minr[0]
    rgb.append(ranger)

    maxg = max(l,key=lambda x:x[1])
    ming = min(l,key=lambda x:x[1])
    rangeg = maxg[1] - ming[1]
    rgb.append(rangeg)

    maxb = max(l,key=lambda x:x[2])
    minb = min(l,key=lambda x:x[2])
    rangeb = maxb[2] - minb[2]
    rgb.append(rangeb)

    return rgb.index(max(rgb))

'''
After we get which channel has largest channel, we will sort the list l by this channel c and get the median
'''
def taker(l):
    return l[0]
def takeg(l):
    return l[1]
def takeb(l):
    return l[2]

def median(l,c):
    if c==0:
        sl=sorted(l, key=taker)
    elif c==1:
        sl=sorted(l, key=takeg)
    else:
        sl=sorted(l, key=takeb)

    '''
    After sort the list by channel, we need to split the sl into two lists: sl1 and sl2. And get the means RGB for each part
    '''
    n = len(l)
    sl1=sl[0:n//2]
    sl2=sl[n//2:n]
    mean1=np.mean(sl1,axis=0)
    mean2=np.mean(sl2,axis=0)
    mean1=mean1.astype(int)
    mean2=mean2.astype(int)

    if n%2==1:
        return sl[n//2],mean1,mean2
    else:
        a=sl[n//2-1]
        b=sl[n//2]
        m0=(a[0]+b[0])/2
        m1=(a[1]+b[1])/2
        m2=(a[2]+b[2])/2
        return[m0,m1,m2],mean1,mean2


'''
Go through all pixels in the image, if its c channel less than median's c channel, set it color = mean1, else color = mean2
'''
def depth1(img):
    l=tolist(img)
    c=maxrange(l)

    med,mean1,mean2=median(l,c)
    h,w,cn=img.shape
    for i in range(h):
        for j in range(w):

            if img[i][j][c]<=med[c]:
                img[i][j]=mean1
            else:
                img[i][j]=mean2

    cv2.imshow("1-bit",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

depth1(img)




#cv2.imshow("8-bits",img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#maxrange_channel(img)





#xp=[[1,2,5],[3,4,88],[4,6,0],[4444,1,12]]
#print median(xp,0)

#print np.mean(xp,axis=0)
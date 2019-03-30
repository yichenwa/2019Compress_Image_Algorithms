import cv2
import numpy as np
# author Yichen Wang

img = cv2.imread("/Users/saber/Desktop/Project_yichen/t1.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)#convert to grayscale

def cal_mu(l,t):#calcuate mu (gray_list, threshold)
    mu1 = 0 #(pixels less than t)
    size1=0
    mu2 = 0 #(pixels larger than t)
    size2=0
    for i in range (len(l)):
        if i<=t:
            mu1 += i * len(l[i])
            size1 += len(l[i])
        else:
            mu2 += i * len(l[i])
            size2 += len(l[i])
    if size1==0:
        mu1 = 0
    else:
        mu1 = mu1/size1
    if size2==0:
        mu2=0
    else:
        mu2 = mu2/size2
    return mu1, mu2

def cal_weight(l,t,h,w): #calcuate weight of two classes
    weight1 = 0;
    weight2 = 0;
    for i in range (len(l)):
        if i<=t:
            weight1 += len(l[i])
        else:
            weight2 += len(l[i])

    return weight1,weight2


'''
Step1: get Histogram and probability
'''
h,w = gray.shape
gray_list=[[] for i in range(256)]
for i in range(0,h):
    for j in range (0,w):
        gray_list[gray[i][j]].append((i,j))


'''
Step 2: we need to find the threshold t makes within class variance minmum, there are 256 possible t.
within class variance = wight of class1 * sigma_sqr1 + wight of class2 * sigma_sqr2
within class variance = total variance - between class variance, so we can find the max between class variance
Ostu find between class variance = wight1*wight2*(mu1-mu2)^2
'''
bcv_list = []
t_list = []
for t in range(1,255):
    mu1,mu2 = cal_mu(gray_list,t)
    w1,w2 = cal_weight(gray_list,t,h,w)
    b = w1*w2*((mu1-mu2)*(mu1-mu2))
    bcv_list.append(b)
    t_list.append(t)

maxb_index = bcv_list.index(max(bcv_list))
t = t_list[maxb_index]
print ("best threshold is ",t)


'''
Step3: pixel <= t set to be white, pixel > t set to be black
'''
for i in range(h):
    for j in range(w):
        if gray[i][j]<=t:
            gray[i][j]=0
        else:
            gray[i][j]=255



cv2.imshow("Ostu_image",gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
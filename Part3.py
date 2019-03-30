import cv2
import numpy as np
# author Yichen Wang


img = cv2.imread("/Users/saber/Desktop/Project_yichen/t1.jpg")
def median_cut(img,i_list):
    #i_list is the list of pixel's index, convert it to a list of pixel color value c_list
    c_list=[]
    for sub_i in i_list:
        i0=sub_i[0]#h
        i1=sub_i[1]#w
        c_list.append(img[i0][i1].tolist())

    #compare the largest range of each channel and decide which channel cc to be choosen
    #Red
    maxR = max(c_list, key=lambda x: x[0])[0]
    minR = min(c_list, key=lambda x: x[0])[0]
    rR = maxR-minR
    #Green
    maxG = max(c_list, key=lambda x: x[1])[1]
    minG = min(c_list, key=lambda x: x[1])[1]
    rG = maxG - minG
    #Blue
    maxB = max(c_list, key=lambda x: x[2])[2]
    minB = min(c_list, key=lambda x: x[2])[2]
    rB = maxB - minB
    rgb = [rR,rG,rB]
    cc = rgb.index(max(rgb))

    #if cc=0/1/2, use R/G/B channel to sort the pixels in this bucket, the sorted result store as s_list
    s_list = sorted(c_list, key=lambda x:x[cc])

    #find the median value m_cc on cc channel
    len_s = len(s_list)
    if len_s%2 == 1:
        m_cc = s_list[len_s//2]
    else:
        s1 = s_list[len_s//2-1]
        s2 = s_list[len_s//2]
        s_sum = list(map(sum,zip(*[s1,s2])))
        m_cc = [x//2 for x in s_sum]

    #use the median value to split i_list into two part. i_less, i_larger, return [i_less,i_larger] as i_sub
    i_less=[]
    i_larger=[]
    for sub_i in i_list:
        i=sub_i[0]#h
        j=sub_i[1]#w
        if img[i][j][cc]<= m_cc[cc]:
            i_less.append([i,j])
        else:
            i_larger.append([i,j])
    return [i_less, i_larger]


def setcolor(i_list_list,img):
    for i_list in i_list_list:
        # when we have a pixel index list, convert it to pixel color value list,
        c_list = []
        for sub_i in i_list:
            i0 = sub_i[0]  # h
            i1 = sub_i[1]  # w
            c_list.append(img[i0][i1].tolist())
        # get the mean value, and set all pixel in the bucket color=mean
        mean = np.mean(c_list, axis=0)
        for sub_i in i_list:
            i0 = sub_i[0]  # h
            i1 = sub_i[1]  # w
            img[i0][i1] = mean




def bit_n(img,n):
    h, w, c = img.shape
    i_list = [[i, j] for i in range(h) for j in range(w)]
    if n==1:
        i_sub = median_cut(img, i_list)
        setcolor(i_sub,img)
        cv2.imshow("bit-1",img)
    if n==2:
        l=[]
        i_sub = median_cut(img, i_list)
        for si_sub in i_sub:
            ii_sub=median_cut(img, si_sub)
            for sii_sub in ii_sub:
                l.append(sii_sub)
        setcolor(l,img)
        cv2.imshow("bit-2",img)
    if n==4:
        l=[]
        i_sub = median_cut(img, i_list)
        for si_sub in i_sub:
            ii_sub=median_cut(img, si_sub)
            for sii_sub in ii_sub:
                iii_sub = median_cut(img,sii_sub)
                for siii_sub in iii_sub:
                    iv_sub = median_cut(img,siii_sub)
                    for siv_sub in iv_sub:
                        l.append(siv_sub)
        setcolor(l,img)
        cv2.imshow("bit-4",img)
    if n==8:
        l=[]
        i_sub = median_cut(img, i_list)
        for si_sub in i_sub:
            ii_sub=median_cut(img, si_sub)
            for sii_sub in ii_sub:
                iii_sub = median_cut(img,sii_sub)
                for siii_sub in iii_sub:
                    iv_sub = median_cut(img,siii_sub)
                    for siv_sub in iv_sub:
                        v_sub = median_cut(img, siv_sub)
                        for sv_sub in v_sub:
                            vi_sub = median_cut(img, sv_sub)
                            for svi_sub in vi_sub:
                                vii_sub = median_cut(img,svi_sub)
                                for svii_sub in vii_sub:
                                    viii_sub = median_cut(img, svii_sub)
                                    for sviii_sub in viii_sub:
                                        l.append(sviii_sub)
        setcolor(l,img)
        cv2.imshow("bit-8",img)


img1=img.copy()
img2=img.copy()
img4=img.copy()
img8=img.copy()
bit_n(img1,1)
bit_n(img2,2)
bit_n(img4,4)
bit_n(img8,8)

cv2.waitKey(0)
cv2.destroyAllWindows()


















#it=[[j,i]for j in range(3) for i in range(5)]
#print it
#it=[[3,400],[120,22]]
#median_cut(img,it)
#a=[1,3,4]
#b=[9,10,5]
#print list(map(sum,zip(*[a,b])))/2
#print sorted(it, key=lambda x:x[0])
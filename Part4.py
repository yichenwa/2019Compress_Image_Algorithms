import cv2
import numpy as np
# author Yichen Wang


img = cv2.imread("/Users/saber/Desktop/Project_yichen/t1.jpg")

'''
I want to implement Octree Color Quantization
0-(0,0,0) 1-(0,0,1) 2-(0,1,0) 3-(0,1,1)
4-(1,0,0) 5-(1,0,1) 6-(1,1,0) 7-(1,1,1)

1st level has 1 leafs
2nd level has 8 leafs
3rd level has 64 leafs
4th level has 512 leafs
As we want to get the results with bit-depth 1(2), 2(4), 4(16), 8(256). 
The tree we create's depth=3 (level4)

'''
def first_3(c):
    #c is the receive color value on one channel, return its first 3 bits of 8 bits
    if c < 32:
        return [0,0,0]
    elif c <64:
        return [0,0,1]
    elif c <96:
        return [0,1,0]
    elif c <128:
        return [0,1,1]
    elif c <160:
        return [1,0,0]
    elif c <192:
        return [1,0,1]
    elif c <224:
        return [1,1,0]
    else:
        return [1,1,1]

def place(r3,g3,b3):
    p_l=[]
    for i in range(3):
        ip_l=[]
        ip_l.append(r3[i])
        ip_l.append(g3[i])
        ip_l.append(b3[i])
        p_l.append(ip_l)
    #the value in ith sublist of p_l is the  index to store the value in i+1 level of tree
    i3=[]
    for iip in p_l:
        a = iip[0]*4 + iip[1]*2 + iip[2]*1
        i3.append(a)
    return i3

def closestc(i,l):
    #for those apperance time very small color, find the closest color
    cl=[]
    for il in l:
        iil=il[1]
        d0 = abs(iil[0]-i[0])
        d1 = abs(iil[1]-i[1])
        d2 = abs(iil[2]-i[2])
        cl.append([d0,d1,d2])
    cc=cl.index(min(cl))
    return l[cc][1]




def octree(img,bits):
    #create the 2nd level of tree, has 8 leafs
    tree = [[] for i in range(8)]
    #create the 3rd level of tree, append 8 leafs in each leaf of 2nd level
    for leaf in tree:
       for i in range(8):
           leaf.append([])
    #create the 4rd level
    for leaf in tree:
        for i_leaf in leaf:
            for i in range(8):
                i_leaf.append([])
    #We get a [8[8[8[]]]] list tree now
    #Go through all pixel in img, get its R,G,B value
    h,w,c=img.shape
    for hi in range(h):
        for wi in range(w):
            rgb=img[hi][wi].tolist()
            rc=rgb[0]
            gc=rgb[1]
            bc=rgb[2]
            #convert its C channel vlaue to first 3-bits of 8-bits C.
            r3=first_3(rc)
            g3=first_3(gc)
            b3=first_3(bc)
            #find the place it should be placed in 512 leafs
            i3 = place(r3,g3,b3)
            tree[i3[0]][i3[1]][i3[2]].append([hi,wi])
    # Calculate each leafs len in the tree
    l_size=[]
    for i in range(8):
        for ii in range(8):
            for iii in range(8):
                l_size.append([len(tree[i][ii][iii]),[i,ii,iii]])
    l_size = sorted(l_size, key=lambda x: x[0], reverse=True)
    #we want the first 2^bits lists
    sl=l_size[:2**bits]
    nl=l_size[2**bits:]
    #bound=l_size[2**bits]

    for i in sl:
        lp = i[1]
        p1 = lp[0]
        p2 = lp[1]
        p3 = lp[2]
        c_l=[]
        for leaf in tree[p1][p2][p3]:
            c_l.append(img[leaf[0]][leaf[1]].tolist())
        mean = np.mean(c_l, axis=0)
        for leaf in tree[p1][p2][p3]:
            img[leaf[0]][leaf[1]] = mean

    for i in nl:
        lp = i[1]
        if i[0]!=0:
            p1 = lp[0]
            p2 = lp[1]
            p3 = lp[2]
            cc = closestc([p1,p2,p3],sl)
            cc_leaf = tree[cc[0]][cc[1]][cc[2]]
            c1=cc_leaf[0][0]
            c2=cc_leaf[0][1]
            ccc=img[c1][c2].tolist()
            for leaf in tree[p1][p2][p3]:
                img[leaf[0]][leaf[1]] = ccc

    cv2.imshow(str(bits),img)






img1=img.copy()
img2=img.copy()
img4=img.copy()
img8=img.copy()
octree(img1,1)
octree(img2,2)
octree(img4,4)
octree(img8,8)

cv2.waitKey(0)
cv2.destroyAllWindows()
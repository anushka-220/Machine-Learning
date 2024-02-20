import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from PIL import Image
from sklearn.cluster import KMeans
#Non Local Means
img = cv.imread(r"gui\1_phase.jpg")
d = cv.fastNlMeansDenoisingColored(img,None,5,5,3,10)

im=Image.open(r"gui\1_phase.jpg")
im_array = np.array(im)
im_array = cv.fastNlMeansDenoisingColored(im_array,None,5,5,3,10)
dst = im_array.copy() #
# pix=im.load()
w,h= im.size
pix_val=list((Image.fromarray(im_array)).getdata())
channels=3
pix_val= np.array(pix_val).reshape((w,h,channels))
print(pix_val)
print (im.size)

#using k means clustering

clt=KMeans(n_clusters=5) #clusteirng object
clt.fit(dst.reshape(-1,3))
print(clt.labels_)
print(clt.cluster_centers_)

for i, center in enumerate(clt.cluster_centers_):
    print(f"Cluster {i+1}: RGB = {center}")
    
def palette(clusters):
    width=300
    palette = np.zeros((50, width, 3), np.uint8)
    steps = width/clusters.cluster_centers_.shape[0]
    for idx, centers in enumerate(clusters.cluster_centers_): 
        palette[:, int(idx*steps):(int((idx+1)*steps)), :] = centers
    return palette

clt1= clt.fit(dst.reshape(-1,3))
# plt.subplot(221), plt.imshow(dst)
plt.subplot(121),plt.imshow(palette(clt1))

for y in range (0,h):
    for x in range (0,w):
        pixel_array=pix_val[x,y]
        r=pixel_array[0]
        g=pixel_array[1]
        b=pixel_array[2] 
        if ((175<= r <= 185) or (80 <= g <= 90) or (10<= b <= 20)) or ((145 <= r <= 155) or (55 <= g <= 65) or (0 <= b <= 10)):
            pix_val[x,y] = [222,131,45]
        if((249<= r<=257) or (197<=g<=203) or (104<=b<=107)  ):
            pix_val[x,y]= [235,168,75]
new_image= Image.fromarray(pix_val.astype('uint8'), 'RGB')

# plt.subplot(223), plt.imshow(dst)
plt.subplot(122),plt.imshow(new_image)
plt.show()
    #231,147,56


#plt.subplot(121),plt.imshow(img)
#plt.subplot(122),plt.imshow(dst)
#plt.show()

## getting rgb value of all the pixels to know the range

''' image=Image.fromarray(img)
img_temp= img.copy()

print(img.shape)
print(img)

print(img.reshape(-1,3).shape)
print(img.reshape(-1,3))

unique, counts= np.unique(img.reshape(-1,3), axis=0, return_counts= True)
print("unique=", unique)
print("counts=", counts)

img_temp[:, :, 0], img_temp[:,:, 1], img_temp[:, :, 2]= unique[np.argmax(counts)]

plt.subplot(121), plt.imshow(img)
plt.subplot(122),plt.imshow(img_temp)
plt.show() '''



old_color= [46.60958713, 133.49285768, 223.93499179]
new_color= [55.55619913, 146.47444827, 229.82860425]

'''
h,w,channel= np.shape(d)
mask= np.zeros((h,w))
mask=[[1 if np.all(channel==[old_color]) else 0 for channels in row] for row in d]

mask=np.array(mask)
x,y =np.where(mask>0)
d[x,y, :]=new_color

#d[np.all( d== (1.0814951, 60.71507353 ,165.57965686), axis=None)]== (34.32200373 ,115.4999783 , 212.61422928)

plt.subplot(121), plt.imshow(dst)
plt.subplot(122),plt.imshow(d)
plt.show()'''

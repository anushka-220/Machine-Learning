import numpy as np
import cv2
import math

#Read image in grayscale
#0 denotes grayscale

#change the path to your own machine
img=cv2.imread('D:\\Pranav\\Pictures\\Saved Pictures\\1_amplitude.jpg', 0)

#retrieve the dimensions of the image
#hh= height, ww= width of the image
hh, ww = img.shape

#get min max and mean value of image
img_min = np.amin(img)
img_max = np.amax(img)
img_mean = int(np.mean(img))

#Padding the image : adding extra pixels around 
# pad the image to dimension a power of 2

#calculate smallest power of 2 >= hh
hhh = math.ceil(math.log2(hh))
hhh = int(math.pow(2,hhh))

www = math.ceil(math.log2(ww))
www = int(math.pow(2,www))

#create padded image
#create numpy aray with dimensions (hhh,www) filled with img_mean
imgp = np.full((hhh,www), img_mean, dtype=np.uint8)

#copy original image to the top left corner of the padded image
imgp[0:hh, 0:ww] = img

#new image has dimensions (hhh, wwww)

#WHY POWER OF 2? 
# most efficient for fft 

# convert image to floats and do dft saving as complex output
dft = cv2.dft(np.float32(imgp), flags = cv2.DFT_COMPLEX_OUTPUT)

# apply shift of origin from upper left corner to center of image
dft_shift = np.fft.fftshift(dft)

# extract magnitude and phase images
mag, phase = cv2.cartToPolar(dft_shift[:,:,0], dft_shift[:,:,1])

# get spectrum
spec = np.log(mag) / 20
min, max = np.amin(spec, (0,1)), np.amax(spec, (0,1))

# threshold the spectrum to find bright spots
thresh = (255*spec).astype(np.uint8)
thresh = cv2.threshold(thresh, 155, 255, cv2.THRESH_BINARY)[1]

# cover the center rows of thresh with black
yc = hhh // 2
cv2.line(thresh, (0,yc), (www-1,yc), 0, 5)

# get the y coordinates of the bright spots
points = np.column_stack(np.nonzero(thresh))
print(points)

# create mask from spectrum drawing horizontal lines at bright spots
mask = thresh.copy()
for p in points:
    y = p[0]
    cv2.line(mask, (0,y), (www-1,y), 255, 5)
    
# apply mask to magnitude such that magnitude is made black where mask is white
mag[mask!=0] = 0

# convert new magnitude and old phase into cartesian real and imaginary components
real, imag = cv2.polarToCart(mag, phase)

# combine cartesian components into one complex image
back = cv2.merge([real, imag])

# shift origin from center to upper left corner
back_ishift = np.fft.ifftshift(back)

# do idft saving as complex output
img_back = cv2.idft(back_ishift)

# combine complex components into original image again
img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])

# crop to original size
img_back = img_back[0:hh, 0:ww]

# re-normalize to 8-bits in range of original
min, max = np.amin(img_back, (0,1)), np.amax(img_back, (0,1))
notched = cv2.normalize(img_back, None, alpha=img_min, beta=img_max, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

cv2.imshow("ORIGINAL", img)
cv2.imshow("PADDED", imgp)
cv2.imshow("MAG", mag)
cv2.imshow("PHASE", phase)
cv2.imshow("SPECTRUM", spec)
cv2.imshow("THRESH", thresh)
cv2.imshow("MASK", mask)
cv2.imshow("NOTCHED", notched)
cv2.waitKey(0)
cv2.destroyAllWindows()


# write result to disk
cv2.imwrite("pattern_lines_spectrum.png", (255*spec).clip(0,255).astype(np.uint8))
cv2.imwrite("pattern_lines_thresh.png", thresh)
cv2.imwrite("pattern_lines_mask.png", mask)
cv2.imwrite("pattern_lines_notched.png", notched)



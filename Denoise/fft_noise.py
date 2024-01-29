import cv2
import numpy as np
from matplotlib import pyplot as plt
'''
Read the image





kernel=np.ones((3,3),np.float32)/9
filt_2D=cv2.filter2D(img, -1, kernel)
blur=cv2.blur(filt_2D,(3,3))
gaussian_blur=cv2.GaussianBlur(blur, (3,3), 0)
median_blur=cv2.medianBlur(gaussian_blur,3)

cv2.imshow("Original",img)
cv2.imshow("2D custom filter", filt_2D)
cv2.imshow("Blur", blur)
cv2.imshow("Gaussian Blur", gaussian_blur)
cv2.imshow("Median Blur", median_blur)
cv2.waitKey(0) 

import time
import os
from pyvsnr import vsnr 
vsr= vsnr(img.shape)
img = cv2.imread('C:\\Users\\ANUSHKA SINGH\\Downloads\\1_amplitude.jpg')

print(vsr)
def ex_camera_stripes(noise_level=100, sigma=(1000, 0.1), theta=0,
                      show_plot=False):
    """
    Example of stripes removal from 'camera' image
    """
    label = "camera_stripes"
    filters = [{'name': 'Gabor',
                'noise_level': noise_level, 'sigma': sigma, 'theta': theta}]
    return img_process(label, filters, show_plot=show_plot)

def img_process(label, filters, show_plot=False):
    """ Image processing"""
    print(f"{label}...", end=" ")

    # vsnr processing
    t0 = time.process_time()
    img_corr = vsnr2d(img, filters, nite=20)
    print("CGPU running time :", time.process_time() - t0)

    # image renormalization
    img_corr = np.clip(img_corr, img.min(), img.max())
    fig = plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.title("Original")
    plt.imshow(img, cmap='gray')
    plt.subplot(122)
    plt.title("Corrected")
    plt.imshow(img_corr, cmap='gray')
    plt.tight_layout()
    plt.show()

    
        
        

    return img_corr
   
ex_camera_stripes()

'''
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Read the image
f = cv2.imread('D:\\Pranav\\Pictures\\Saved Pictures\\1_amplitude.jpg', cv2.IMREAD_GRAYSCALE)

# Display the original image
plt.imshow(f, cmap='gray')
plt.title('f')
plt.show()

# Perform FFT
m = max(f.shape)
P = 2**int(np.ceil(np.log2(2 * m)))
PQ = [P, P]

Fp = np.fft.fft2(f, s=PQ)

# Shift the zero frequency component to the center
Fc = np.fft.fftshift(Fp)
Fc_abs = np.abs(Fc)
Fs_log = np.log(1 + Fc_abs)

# Display the magnitude spectrum
plt.imshow(Fc_abs, cmap='gray')
plt.title('Fc (abs)')
plt.show()

# Display the log-transformed spectrum
plt.imshow(Fs_log, cmap='gray')
plt.title('Fs (log)')
plt.show()

# Read the spectral mask
Hp = cv2.imread('spec-mask.png', cv2.IMREAD_GRAYSCALE) / 255.0
#it messes up here ^

# Perform element-wise multiplication in the frequency domain
Gp = Hp * Fp

# Perform inverse FFT
gp = np.real(np.fft.ifft2(Gp))

# Crop the result to the size of the original image
gpc1 = gp[:f.shape[0], :f.shape[1]]

# Display the processed image
plt.imshow(gpc1, cmap='gray')
plt.title('g')
plt.show()

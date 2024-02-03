import numpy as np
from PIL import Image
from scipy.ndimage import convolve
import matplotlib.pyplot as plt
def read_image(image_path):
    img = Image.open(image_path).convert('L')  # Convert to grayscale
    img_array = np.array(img)
    return img_array

def laplacian(image):
    #This was provided in the paper itself
    laplacian_operator = np.array([[-1, -1, -1],
                                   [-1, 8, -1],
                                   [-1, -1, -1]])
    laplacian_image = np.abs(convolve(image.astype(float), laplacian_operator, mode='constant'))
    return laplacian_image

def heterogeneity_func(image):
    # Logarithm of the image intensity
    log_intensity = np.log1p(image)

    # Laplacian of LogF (abrupt change in intensity)
    laplacian_log = laplacian(log_intensity)

    # Normalize Laplacian values
    L_min = np.min(laplacian_log)
    L_max = np.max(laplacian_log)
    normalized_laplacian = (laplacian_log - L_min) / (L_max - L_min)

    # Normalize intensity values
    I_min = np.min(log_intensity)
    I_max = np.max(log_intensity)
    normalized_intensity = (log_intensity - I_min) / (I_max - I_min)

    heterogeneity = normalized_laplacian * normalized_intensity

    return heterogeneity

image_path = r"D:\\Pranav\\Pictures\\Saved Pictures\\1_amplitude.jpg"
image = read_image(image_path)

heterogeneity_result = heterogeneity_func(image)
print(heterogeneity_result)
plt.imshow(heterogeneity_result)
plt.show()

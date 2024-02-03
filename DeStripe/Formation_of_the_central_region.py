import numpy as np
from scipy.ndimage import label, find_objects
from scipy.ndimage.measurements import center_of_mass

from heterogeneity import *
from Global_Sampling_of_Pixels import read_image, heterogeneity_func, global_pixel_sampling



def formation_central_region(Pn1):
    # Calculate the moment of inertia tensor
    #here we have used the covariance matrix
    inertia_tensor = np.cov(Pn1, rowvar=False) #CHECK THIS LATER

    #eigenvalues and eigenvectors of the tensor
    eigenvalues, eigenvectors = np.linalg.eigh(inertia_tensor)

    # Extract the major and minor axes lengths (σx, σy)
    sigma_x, sigma_y = np.sqrt(eigenvalues) # CHECK THIS LATER

    initial_radius = np.sqrt(sigma_x + sigma_y)

    # Find the center of mass of Pn1
    center_i, center_j = map(int, center_of_mass(np.ones_like(Pn1), labels=Pn1, index=1))

    # Initialize central region and off-center region
    central_region = np.zeros_like(Pn1)
    off_center_region = np.copy(Pn1)

    # Expand the central region outwardly
    current_radius = 0
    while current_radius < initial_radius:
        current_radius += initial_radius / 10

        #circular mask centered at (center_i, center_j) i.e. the center of mass
        y, x = np.ogrid[:Pn1.shape[0], :Pn1.shape[1]]
        mask = ((x - center_j) ** 2 + (y - center_i) ** 2) <= current_radius ** 2

        # Label connected components in the mask
        labeled_mask, num_labels = label(mask)

        # label corresponding to the central region
        central_label = labeled_mask[center_i, center_j]

        # Count Pn1 pixels and total pixels within the region
        pixels_in_region = Pn1 * mask
        total_pixels = np.sum(mask)

        # If the ratio is <= 0.85, stop the expansion
        if total_pixels > 0 and np.sum(pixels_in_region) / total_pixels <= 0.85:
            break

        # Include the visited pixels as members in the central region
        central_region += (labeled_mask == central_label)

    # Form Pn2 as Pn1 - C0
    off_center_region -= central_region

    return central_region, off_center_region

image_path = r"C:\Users\ANUSHKA SINGH\Downloads\1_amplitude.jpg"
image = read_image(image_path)

# Assuming Pn1 is already obtained from the previous steps
Pn1 = global_pixel_sampling(image)

# Form the central region and off-center region
central_region, off_center_region = formation_central_region(Pn1)
print (off_center_region.shape)

# Display or process central_region and off_center_region as needed

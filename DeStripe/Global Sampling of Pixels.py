import numpy as np
from PIL import Image
from scipy.ndimage import convolve
from heterogeneity import *

def global_pixel_sampling(image):
    # Step 1: Calculate H values of LogF
    log_intensity = np.log1p(image)
    laplacian_log = laplacian(log_intensity)

    # Step 2: Form the histogram of H with 20 bins and variation within 0.05
    bin_width = 0.05
    num_bins = int((np.max(laplacian_log) - np.min(laplacian_log)) / bin_width)
    
    hist, bin_edges = np.histogram(laplacian_log, bins=num_bins)

    # Step 3: Find the most spreading group of consecutive bins with non-zero populations
    non_zero_bins = np.nonzero(hist)[0]
    consecutive_groups = np.split(non_zero_bins, np.where(np.diff(non_zero_bins) != 1)[0] + 1)

    most_spreading_group = max(consecutive_groups, key=len)

    # Step 4: Find the threshold bin in the direction of increasing heterogeneity
    threshold_bin = most_spreading_group[0]
    for bin_index in most_spreading_group:
        if hist[bin_index] / hist[most_spreading_group[-1]] <= 0.5:
            threshold_bin = bin_index
            break

    # Step 5: Calculate the H threshold as H_ref = 0.5 * (H_up + H_low)
    H_ref = 0.5 * (bin_edges[threshold_bin] + bin_edges[threshold_bin + 1])

    # Step 6: Calculate the intensity threshold as I_ref = 0.5 * (max_ref + ave_ref)
    mask = laplacian_log > H_ref
    selected_pixels = log_intensity[mask]
    I_ref = 0.5 * (np.max(selected_pixels) + np.mean(selected_pixels))

    # Step 7: Pn1 = {(i, j)| H(i, j) > H_ref & I(i, j) > I_ref }
    Pn1 = np.argwhere((laplacian_log > H_ref) & (log_intensity > I_ref))

    return Pn1

image_path = r"C:\Users\ANUSHKA SINGH\Downloads\1_amplitude.jpg"
image = read_image(image_path)

sampled_pixels = global_pixel_sampling(image)
print("Sampled Pixels (Pn1):", sampled_pixels)


    
    
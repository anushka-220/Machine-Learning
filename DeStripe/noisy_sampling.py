from heterogeneity import *
from scipy.ndimage.measurements import center_of_mass
import numpy as np
import scipy.optimize as opt
from Formation_of_the_central_region import *

e = 2.71828

def objective_function_sum(Pn1,c1,c2):
    center_i, center_j = map(int, center_of_mass(np.ones_like(Pn1), labels=Pn1, index = 1))
    intensity_center = image[center_i, center_j]
    summation = 0
    eigenvalues, eigenvectors = np.linalg.eigh
    for i in range(Pn1.shape[0]):
        for j in range(Pn1.shape[1]):
            intensity = image[i,j]
            f_ij = (intensity / intensity_center) - (e ** (-(c1 * ((i - center_i) ** 2) / eigenvalue_x_dash) - (c2 * ((j - center_j) ** 2) / eigenvalue_y_dash)))
            summation += f_ij
    return summation

def new_eigenvals(old_eigenval_x, old_eigenval_y):
    pass

result = opt.minimize(objective_function_sum)

central_region, off_center_region = formation_central_region(Pn1)

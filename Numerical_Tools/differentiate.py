import numpy as np

# derivative = differentiate_vector(x_vector, y_vector):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## x_vector: array of length n containing the x-values; need not be evenly spaced.
## y_vector: array of length n containing the y-values.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## derivative: the derivative dy/dx, length n, computed using a central difference scheme with forward/backward
## difference at the respective boundaries.


def differentiate_vector(x_vector, y_vector):
    # Forward difference and backward difference at boundaries; central difference for mid-values:
    derivative = np.zeros_like(y_vector)
    for i in range(len(y_vector)):
        ## At left boundary, use forward difference:
        if i == 0:
            derivative[i] = (y_vector[i] + y_vector[i+1]) / (x_vector[i+1] - x_vector[i])
        ## At right boundary, use backward difference:
        elif i == (len(y_vector) - 1):
            derivative[i] = (y_vector[i] + y_vector[i-1]) / (x_vector[i] - x_vector[i-1])
        ## At mid-values, use central difference:
        else:
            derivative[i] = (y_vector[i-1] + y_vector[i] + y_vector[i+1]) / (x_vector[i+1] - x_vector[i-1])
    return derivative







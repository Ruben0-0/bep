import numpy as np
from scipy import stats


# y = skewed_norm_pdf(x, a, mu, sigma):
# =====================================================================================================
# INPUT:
# =====================================================================================================
## x: array containing the x-range over which the pdf is computed.
## a: a measure of skewness. If a>0, pdf is positively skewed. If a<0, pdf is negatively skewed.
## mu: the mean of the skewed distribution.
## sigma: the standard deviation of the skewed distribution.
# =====================================================================================================
# OUTPUT:
# =====================================================================================================
## y: array, same length as 'x', containing the skewed normal distribution PDF.


def skewed_norm_pdf(x, a, mu, sigma):
    # Calculate mean for a skewed normal distribution using scipy's skewednorm function:
    shifted_mean = stats.skewnorm.mean(a, loc=mu, scale=sigma)
    # Calculate the correct loc input to obtain a mean of 'mu':
    mu_corrected = mu - (shifted_mean - mu)
    # Now calculate the full skewed normal distribution with correct mean:
    y = stats.skewnorm.pdf(x, a, loc=mu_corrected, scale=sigma)
    return y


# y = skewed_norm_rvs(a, mu, sigma):
# =====================================================================================================
# INPUT:
# =====================================================================================================
## a: a measure of skewness. If a>0, pdf is positively skewed. If a<0, pdf is negatively skewed.
## mu: the mean of the skewed distribution.
## sigma: the standard deviation of the skewed distribution.
# =====================================================================================================
# OUTPUT:
# =====================================================================================================
## y: random variable from the skewed normal distribution.


def skewed_norm_rvs(a, mu, sigma):
    # Calculate mean for a skewed normal distribution using scipy's skewednorm function:
    shifted_mean = stats.skewnorm.mean(a, loc=mu, scale=sigma)
    # Calculate the correct loc input to obtain a mean of 'mu':
    mu_corrected = mu - (shifted_mean - mu)
    # Grab a random variable from the skewed normal distribution with correct mean:
    y = stats.skewnorm.rvs(a, loc=mu_corrected, scale=sigma, size=1)
    return y[0]

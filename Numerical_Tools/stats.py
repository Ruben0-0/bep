from scipy import stats


# y = skewed_norm_pdf(x, a, mu, sigma):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## x: array containing the x-range over which the pdf is computed.
## a: a measure of skewness. If a>0, pdf is positively skewed. If a<0, pdf is negatively skewed.
## mu: the mean of the skewed distribution.
## sigma: the standard deviation of the skewed distribution.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## y: array, same length as 'x', containing the skewed normal distribution PDF.
## mu_corrected: the mean of the skewed distribution displaced such that it aligns with Scipy's PDF 'loc' parameter.


def skewed_norm_pdf(x, a, mu, sigma):
    # Calculate mean for a skewed normal distribution using scipy's skewednorm function:
    shifted_mean = stats.skewnorm.mean(a, loc=mu, scale=sigma)
    # Calculate the correct loc input to obtain a mean of 'mu':
    mu_corrected = mu - (shifted_mean - mu)
    # Now calculate the full skewed normal distribution with correct mean:
    y = stats.skewnorm.pdf(x, a, loc=mu_corrected, scale=sigma)
    return y, mu_corrected


# y = skewed_norm_rvs(a, mu, sigma):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## a: a measure of skewness. If a>0, pdf is positively skewed. If a<0, pdf is negatively skewed.
## mu: the mean of the skewed distribution.
## sigma: the standard deviation of the skewed distribution.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## y: random variable from the skewed normal distribution.


def skewed_norm_rvs(a, mu, sigma):
    # Calculate mean for a skewed normal distribution using scipy's skewnorm function:
    shifted_mean = stats.skewnorm.mean(a, loc=mu, scale=sigma)
    # Calculate the correct loc input to obtain a mean of 'mu':
    mu_corrected = mu - (shifted_mean - mu)
    # Grab a random variable from the skewed normal distribution with correct mean:
    y = stats.skewnorm.rvs(a, loc=mu_corrected, scale=sigma, size=1)
    return y[0]


# y1, y2, p_25, p_75 = pdf_splitter(x, a, mu_corrected, sigma):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## x: array containing the x-range over which the pdf is computed.
## a: a measure of skewness. If a>0, pdf is positively skewed. If a<0, pdf is negatively skewed.
## mu_corrected: the mean of the skewed distribution displaced such that it aligns with Scipy's PDF 'loc' parameter.
## sigma: the standard deviation of the skewed distribution.
# ======================================================================================================================
# OUTPUT:
# =========================================================================================y=============================
## y1: array, same length as 'x', containing the skewed normal distribution PDF with a mean corresponding to P25
##     of the skewed normal distribution with parameters a, mu_corrected, and sigma.
## y2: array, same length as 'x', containing the skewed normal distribution PDF with a mean corresponding to P75
##     of the skewed normal distribution with parameters a, mu_corrected, and sigma.
## p_25: the 25th percentile of the skewed normal distribution with parameters a, mu_corrected and sigma.
## p_75: the 75th percentile of the skewed normal distribution with parameters a, mu_corrected and sigma.


def pdf_splitter(x, a, mu_corrected, sigma):
    # Calculate 25th and 75th percentiles of original PDF:
    p_25 = stats.skewnorm.ppf(0.25, a, loc=mu_corrected, scale=sigma)
    p_75 = stats.skewnorm.ppf(0.75, a, loc=mu_corrected, scale=sigma)
    # Create new distributions with P25 and P75 as means:
    y1, p_25_corrected = skewed_norm_pdf(x, a, mu=p_25, sigma=sigma)
    y2, p_75_corrected = skewed_norm_pdf(x, a, mu=p_75, sigma=sigma)
    # Normalize the distributions:
    y1 /= 2
    y2 /= 2
    return y1, y2, p_25, p_75

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
## psi:
# ======================================================================================================================
# OUTPUT:
# =========================================================================================y============================
## y1: array, same length as 'x', containing the skewed normal distribution PDF with a mean corresponding to P25
##     of the skewed normal distribution with parameters a, mu_corrected, and sigma.
## y2: array, same length as 'x', containing the skewed normal distribution PDF with a mean corresponding to P75
##     of the skewed normal distribution with parameters a, mu_corrected, and sigma.
## mu_left: the left percentile (depending on psi) of the skewed normal distribution with parameters a, mu_corrected
##          and sigma.
## mu_right: the right percentile (depending on psi) of the skewed normal distribution with parameters a, mu_corrected
##           and sigma.


def pdf_splitter(x, a, mu_corrected, sigma, psi):
    # Retrieve the left and right percentile to be used from psi:
    p_left, p_right = psi_function(psi)
    # Calculate left and right percentile values of original PDF:
    mu_left = stats.skewnorm.ppf(p_left, a, loc=mu_corrected, scale=sigma)
    mu_right = stats.skewnorm.ppf(p_right, a, loc=mu_corrected, scale=sigma)
    # Apply the median-to-mean correction (so that psi=0 aligns with the original distribution):
    mean = stats.skewnorm.mean(a, loc=mu_corrected, scale=sigma)
    median = stats.skewnorm.median(a, loc=mu_corrected, scale=sigma)
    mu_left += mean - median
    mu_right += mean - median
    # Create new distributions with mu_left and mu_right as means:
    y1, p_25_corrected = skewed_norm_pdf(x, a, mu=mu_left, sigma=sigma)
    y2, p_75_corrected = skewed_norm_pdf(x, a, mu=mu_right, sigma=sigma)
    # Normalize the distributions:
    y1 /= 2
    y2 /= 2
    return y1, y2, p_left, p_right, mu_left, mu_right


# P_left, P_right = psi_function(psi):
# ======================================================================================================================
# INPUT:
# ======================================================================================================================
## psi: value between 0 - 1; if psi = 1, max spread between left and right percentiles; if psi = 0, both left and right
##      percentiles are P50.
# ======================================================================================================================
# OUTPUT:
# ======================================================================================================================
## P_left: the left percentile.
## P_right: the right percentile.


def psi_function(psi):
    if psi >= (1 - 1e-3):
        psi = 1 - 1e-3
    P_left = 0.5 - 0.5*psi
    P_right = 0.5 + 0.5*psi
    return P_left, P_right

import numpy as np
from scipy.stats import multivariate_normal # used just for comparison

def multivariate_gaussian_pdf(X, Mu, Sigma):
    d = Mu.shape[0] # number of dimensions

    # Center the data
    X_centered = X - Mu

    # inverse and determinant of the covariance matrix
    Sigma_inv = np.linalg.inv(Sigma)
    det_Sigma = np.linalg.det(Sigma)

    # exponent and normalization constant
    exponent = -0.5 * np.sum(X_centered @ Sigma_inv * X_centered, axis=1)
    normalization_constant = 1/ ((2*np.pi)**(d/2)*np.sqrt(det_Sigma))

    # calculate and return pdf values
    return normalization_constant*np.exp(exponent)

# locations
X = [
        [2,2,2], #x1
        [1,4,3], #x2
        [1,1,5]  #x3
    ]

# covariance matrix
Sigma = [
        [4,2,1],
        [2,5,2],
        [1,2,3]
        ]

# mean
Mu = [1,3,5]

# convert lists to np arrays
X = np.array(X)
Sigma = np.array(Sigma)
Mu = np.array(Mu)

# compute and print the pdf values using function implemented by myself and ready-made function for comparison
distribution = multivariate_normal(mean=Mu, cov=Sigma)
pdf_values = distribution.pdf(X)

print('results by function implemented by myself:\n', multivariate_gaussian_pdf(X,Mu,Sigma))

print('results by scipy.stats.multivariate_normal:\n', pdf_values)
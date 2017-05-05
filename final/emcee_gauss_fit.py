#! /usr/bin/python

################################################################################
# This module was written based on a tutorial by Dan Foreman-Mackey and 
# contributors found here http://dan.iel.fm/emcee/current/user/line/ 
################################################################################

import numpy as np
import emcee
import scipy.optimize as op

NDIM = 4

################################################################################
###################### FIT GAUSSIAN USING SCIPY.OPTIMIZE #######################

def gaussian(x, a, mu, sig):
    return a*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def lnlike(theta, x, y, yerr):
	A, mu, sigma, lnf = theta
	model = gaussian(x,A,mu,sigma)
	inv_sigma2 = 1.0/(yerr**2 + model**2*np.exp(2*lnf))
	return -0.5*(np.sum((y-model)**2*inv_sigma2 - np.log(inv_sigma2)))

def findParameters(A0,m0,sigma0,f0):
	nll = lambda *args: -lnlike(*args)
	result = op.minimize(nll, [A0, mu0, sigma0,np.log(f0)], args=(x, y, yerr))
#	A_ml, mu_ml, sigma_ml, lnf_ml = result["x"]
	return result["x"]

# TODO CHANGE THESE VALUES
def lnprior(theta):
	m, b, lnf = theta
	if -5.0 < m < 0.5 and 0.0 < b < 10.0 and -10.0 < lnf < 1.0:
		return 0.0
	return -np.inf

def lnprob(theta, x, y, yerr):
	lp = lnprior(theta)
	if not np.isfinite(lp):
		return -np.inf
	return lp + lnlike(theta, x, y, yerr)

def uncertainties(nwalkers,theta0, x, y, yerr):
	result = findParamete(*theta0)
	pos = [result + 1e-4*np.random.randn(NDIM) for i in range(nwalkers)]
	sampler = emcee.EnsembleSampler(nwalkers, NDIM, lnprob, args=(x, y, yerr))
	sampler.run_mcmc(pos, 500)
	samples = sampler.chain[:, 50:, :].reshape((-1, ndim))
	samples[:, 2] = np.exp(samples[:, 2])
	Amcmc, mumcmc, sigmcmc, fmcmc = map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]),
										zip(*np.percentile(samples, [16, 50, 84],
														   axis=0)))

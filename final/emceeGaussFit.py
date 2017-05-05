#! /usr/bin/python

################################################################################
# This module was written based on a tutorial by Dan Foreman-Mackey and 
# contributors found at http://dan.iel.fm/emcee/current/user/line/ 
################################################################################

import numpy as np
import emcee
import scipy.optimize as op

NDIM = 4

################################################################################
###################### FIT GAUSSIAN USING SCIPY.OPTIMIZE #######################

def gauss(x, p):
	A, mu, sigma = p
	return A*np.exp(-(x-mu)**2/(2.*sigma**2))

def lnlike(theta, x, y, yerr):
	A, mu, sigma, lnf = theta
	model = gauss(x,(A,mu,sigma))
	inv_sigma2 = 1.0/(yerr**2 + model**2*np.exp(2*lnf))
	return -0.5*(np.sum((y-model)**2*inv_sigma2 - np.log(inv_sigma2)))

def findParameters(x,y,yerr,A0,mu0,sigma0,lnf0):
	nll = lambda *args: -lnlike(*args)
	result = op.minimize(nll, [A0, mu0, sigma0, lnf0], args=(x, y, yerr))
#	A_ml, mu_ml, sigma_ml, lnf_ml = result["x"]
	return result["x"]

def lnprior(theta, thetaLower, thetaUpper):
	A, mu, sig, lnf = theta
	AL, muL, sigL, lnfL = thetaLower
	AU, muU, sigU, lnfU = thetaUpper
	if AL < A < AU and muL < mu < muU and lnfL < lnf < lnfU and sigL < sig<sigU:
		return 0.0
	return -np.inf

def lnprob(theta, thetaL, thetaU, x, y, yerr):
	lp = lnprior(theta, thetaL, thetaU)
	if not np.isfinite(lp):
		return -np.inf
	return lp + lnlike(theta, x, y, yerr)

def uncertainties(nwalkers,theta0, thetaL, thetaU, x, y, yerr):
	result = findParameters(x,y,yerr,*theta0)
	print(result)
	pos = [result + 1e-4*np.random.randn(NDIM) for i in range(nwalkers)]
	sampler = emcee.EnsembleSampler(nwalkers, NDIM, lnprob,
                                    args=(thetaL, thetaU, x, y, yerr))
	sampler.run_mcmc(pos, 500)
	samples = sampler.chain[:, 50:, :].reshape((-1, NDIM))
	samples[:, 2] = np.exp(samples[:, 2])
	return map(lambda v: (v[1], v[2]-v[1], v[1]-v[0]), 
			   zip(*np.percentile(samples, [16, 50, 84],axis=0)))

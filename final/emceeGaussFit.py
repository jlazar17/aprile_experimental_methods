#! usr/bin/python

from sys import exit
import numpy as np
try:
	import emcee
except ImportError:
	print('You need to install emcee to use this module. You can install this '
		  'by running the command "sudo easy_install emcee" from the command '
	      'line')
	exit()

# This fits a gaussian with three parameters: amplitude, mean, and standard dev
NDIM = 3

################################################################################
###################### DEFINE LN-LIKELIEHOOD FUNCTION ##########################

def gauss(p, x):
	amp, mu, sigma = p
	return amp*np.exp(-(x-mu)**2/(2.*sigma**2))

def lnlike(p, x, y, yerr):
	amp, mu, sigma = p
	model = gauss(p, x)
	return -0.5*(np.sum((y-model)**2/(yerr**2) + np.log(yerr)))

################################################################################
########################## MONTE-CARLO SIMULATION ##############################

def mcsimulation(pguess, x, y, yerr, n=250):
	# random parameters for the start of each MC simulation
	p0 = [ pguess + 1e-4*np.random.randn(NDIM) for i in range(n) ]
	sampler = emcee.EnsembleSampler(n, NDIM, lnlike, args=[x,y,yerr],a=4)
	# runs a MC simulation for 200 steps as a burn in
	pos, prob, state = sampler.run_mcmc(p0, 200)
	sampler.reset()
	# Resarts the MC smulations from the end of the 200 step burn in
	pos, prob, state = sampler.run_mcmc(pos, 1000, rstate0=state)
	return pos, prob, sampler

################################################################################
################ MANIPULATE MC OUTPUT FOR RELEVANT QUANTITIES ##################

def getStats(pguess, x, y, yerr, nwalkers=250):
	pos, prob, sampler = mcsimulation(pguess, x, y, yerr, n=nwalkers)
	maxprob_indice = np.argmax(prob)
	amp_fit, mu_fit, sigma_fit = pos[maxprob_indice]
	amp_std = sampler.flatchain[:,0].std()
	mu_std = sampler.flatchain[:,1].std()
	sigma_std = sampler.flatchain[:,2].std()
	return amp_fit, mu_fit, sigma_fit, amp_std, mu_std, sigma_std

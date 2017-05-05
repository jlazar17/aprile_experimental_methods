#! usr/bin/python

import matplotlib.pyplot as plt
import pickle
import numpy as np
import emceeGaussFit as gfit

################################################################################
############################## PREPARING ARRAY #################################

a = np.array(pickle.load(open('waveform_integrals.pkl', 'r')))
cutInd = (a >= 30000) & (a <= 35000)
aCut = a[cutInd]

################################################################################
########################### MAKING PLOTTING ARRAYS #############################

n, bins = np.histogram(aCut,bins=50)
binMids = [ (bins[i]+bins[i+1])/2 for i in range(len(bins)-1) ]
binWidth = (bins[1]-bins[0])/2
yErrs = np.array([ x**0.5 for x in n ])


################################################################################
############################# FITTING GAUSSIAN #################################

# numbers based on those in assignment
theta = gfit.findParameters(binMids,n,yErrs,160,32910,879,0.5)
thetaL = (125,31000,700,-10)
thetaU = (200,35000,1000,1)
Amcmc, mumcmc, sigmcmc, lnfmcmc = gfit.uncertainties(100,theta,thetaL,thetaU,
													 binMids,n,yErrs)
print(Amcmc, mumcmc, sigmcmc, lnfmcmc)

################################################################################
################################# PLOTTING #####################################

plt.figure(1)
plt.subplot(111)
plt.errorbar(binMids, n, fmt=' ',xerr = binWidth, yerr = yErrs)
plt.savefig('integral_plt.png')

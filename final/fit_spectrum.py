#! usr/bin/python

import pickle
import numpy as np
import emceeGaussFit as gfit
import matplotlib.pyplot as plt
from matplotlib import rc

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

# numbers based on looking at graph in assignment
guess = (140, 33000, 879)
a, mu, sigma, a_std, mu_std, sigma_std = gfit.getStats(guess, binMids, n, yErrs)
gauss = gfit.gauss((a, mu, sigma), binMids)

################################################################################
################################# PLOTTING #####################################

resultsStr = ('$\mu_{Cs137}=%.2f\pm%.2f ADC Counts$\n$\sigma_{Cs137}='
			  '%.2f\pm%.2f ADC Counts$'%(mu, mu_std, sigma, sigma_std))
plt.figure(1)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rc('text', usetex=True)
fig, ax = plt.subplots(1)
ax.errorbar(binMids, n, fmt=' ',xerr = binWidth, yerr = yErrs)
ax.plot(binMids, gauss, 'r--')
ax.set_title('Fitted Integrals')
ax.set_xlabel('ADC Counts')
ax.set_ylabel('Counts')
ax.text(0.05, 0.95, resultsStr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top')
plt.savefig('integral_plt.png')

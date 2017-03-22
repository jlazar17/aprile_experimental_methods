#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm,poisson
import sys

DATA_FILE = '/Users/yaboijlazar/Documents/School stuff/Experimental_methods/'+sys.argv[1]

def createDataFromInfile(infile):
    with open(infile) as f:
        dataArray = [float(line.rstrip('\n')) for line in f]
    return dataArray

def binData(data, numBins):
    max = np.amax(data)
    min = np.amin(data)
    bins = np.linspace(min, max, int(numBins)+1)
    digitized = np.digitize(data, bins)
    binCount = np.bincount(digitized)[1:]
    binMeans = [data[digitized == i].mean() for i in range(1, len(bins))]
    
def f(prefactor, muGamma, muBKG, muSPE, varBKG, varSPE, gain):
    tmp = poisson(muGamma).pmf(0)*norm(muBKG,sqrt(varBKG)).pdf(gain)
    tmp += poisson(muGamma).pmf(1)*norm(muSPE+muBKG, sqrt(varBKG+varSPE)).pdf(gain)
    tmp += poisson(muGamma).pmf(2)*norm(2*muSPE+muBKG, sqrt(varBKG+2*varSPE)).pdf(gain)
    return prefactor*tmp

def poissonStdDev(mu):
    return (poisson.stats(mu, moments='mvsk'))**.5

def logLikelihood(binCounts, binMeans):
   
def makePlot(xAxis, yAxis):
    yErrs = [poissonStdDev(i) for i in yAxis]
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.figure()
    plt.errorbar(xAxis, yAxis, yerr=yErrs, fmt='.')
    plt.ylabel(r'\textit{Counts (mV)}')
    plt.xlabel(r'\textit{Gain (e^-) (mV)}')
    plt.title('PMT Gain Calibration')
    plt.savefig('foo.png')

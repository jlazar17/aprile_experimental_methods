#! usr/bin/python

import pickle
import matplotlib.pyplot as plt
import numpy as np

def findFII(x,value):
	for i in range(len(x)):
		if x[i]>value:
			index=i
			break
	return index

trace = pickle.load(open('portable_traces.pkl','r'))[1002]
x = np.linspace(1,len(trace),len(trace))

xVLine=[100,2000]

plt.plot(x,trace)
plt.xlabel('ADC Samples')
plt.ylabel('ADC Counts')
plt.title('Waveform 1003')
for i in xVLine:
	plt.axvline(x=i, color='r', linestyle='--')
plt.savefig('waveform_1003.png')

with open('waveform_1003.pkl','w') as f:
	pickle.dump(trace,f)	

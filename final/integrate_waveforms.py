#! usr/bin/python

import numpy as np
import pickle

traces = pickle.load(open('portable_traces.pkl','r'))
a=np.zeros(len(traces))

for i in range(len(traces)):
	trace = traces[i]
	background = np.mean(trace[:100])
	trace_int = trace[100:2001]
	trace_int_wo_bg = trace_int - background
	integral = np.sum(trace_int_wo_bg)
	a[i] = integral
	print(integral)

print(a)

with open('waveform_integrals.pkl','w') as f:
	pickle.dump(a,f)

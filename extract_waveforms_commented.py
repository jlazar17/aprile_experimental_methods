#! usr/bin/python

import pickle as pkl
from bs4 import BeautifulSoup

# inputs are a string and an array of paterns to be removed from that string
def removeText(string, patterns):
	from re import sub
	for pattern in patterns:
		string=sub(pattern,'',string)
	return string

a=[]
soup=BeautifulSoup(open('CsI.xml'), 'xml')
# Finds all instances of the class 'trace' and returns each as a different
# element of an array. There is unwanted text in each thus the term 'dirty'
dirtyTraces=soup.findAll('trace')
for i in range(len(dirtyTraces)):
	# The strings come out in Unicode fomr BeautifulSoup. This converts them to
	# standard Python strings
	_ = str(dirtyTraces[i])
	# Gets rid of the unwanted portions of the text using re.sub. I like this 
	# method over some built in string editing stuff for various reasons, but 
	# do your thing
	_ = removeText(_,['<trace channel="0">','\n </trace>','</trace>'])
	# Splits the string into an array of strings. This is done whenever there is
	# a space
	_ = _.split(' ')
	# Converts each string of the previously created array into a integer
	_ = [ int(x) for x in _ ]
	a.append(_)

with open('portable_traces.pkl','w') as f:
	pkl.dump(a,f)

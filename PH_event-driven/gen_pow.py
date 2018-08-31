import networkx as nx
from sys import argv
from math import sqrt
import random

xmin = 3

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

# return integer power-law numbers capped by k n^1/2

def mypowerlaw_sequence (exponent, size):
	
	expo = -1.0 / (exponent - 1.0)

	xmax = sqrt(size) * xmin * (exponent - 1.0) / (exponent - 2.0)
	
	x = [0] * size
	for i in range(size):
		while True:
			x[i] = int(pow(1.0 - random.random(), expo))
			if x[i] < xmax and x[i] >= xmin:
				break
	return x
	
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

def mypowerlaw (exponent, size):

	deg = mypowerlaw_sequence(exponent, size)
	
	return nx.expected_degree_graph(deg, selfloops = False)

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

if __name__ == "__main__":
	
	if len(argv) != 4:
		print 'usage: python gen_pow.py [size] [exponent] [output name]'
		exit()
	
	n = int(argv[1])
	gamma = float(argv[2])

	G = mypowerlaw(gamma, n)
	
	degseq = G.degree().values()
	s2 = sum([d * d for d in degseq])
	s1 = sum(degseq)
	print 'threshold', str(s1 / (s2 - 2.0 * s1))

	nx.write_edgelist(G, argv[3], data = False)


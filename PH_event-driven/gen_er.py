import networkx as nx
from sys import argv
from scipy.stats import moment
import random

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #

if __name__ == "__main__":
	
	if len(argv) != 4:
		print 'usage: python gen_er.py [n] [m] [output name]'
		exit()
	
	n = int(argv[1])
	m = int(argv[2])
	G = nx.gnm_random_graph(n,m)

	degseq = G.degree().values()
	s2 = sum([d * d for d in degseq])
	s1 = sum(degseq)
	print 'threshold * 1.05:', str(1.05 * s1 / (s2 - 2.0 * s1))

	nx.write_edgelist(G, argv[3], data = False)

#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
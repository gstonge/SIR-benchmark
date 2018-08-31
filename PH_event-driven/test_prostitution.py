from spreading_CR import SpreadingProcess
from timeit import default_timer
import networkx as nx
from numpy.random import randint
from numpy import inf

nsample = 100000

rates = [0.01,0.02,0.04,0.1,0.2,0.4,1,2,4]

G = nx.convert_node_labels_to_integers(nx.read_edgelist('nwk/brazil.lnk'))

for j in range(len(rates)):
	sp = SpreadingProcess(list(G.edges()), rates[j], 1, 0)

	s0 = 0
	start = default_timer()
	for i in range(nsample):
		sources = randint(G.number_of_nodes())
		sp.initialize([sources], i)
		sp.evolve(inf)
		
		s0 += sp.get_Rnode_number_vector()[-1]
		sp.reset()
	stop = default_timer()

	print str(rates[j])
	print str(s0 / float(nsample) / G.number_of_nodes())
	print 'time per outbreak (s)', str((stop - start) / nsample)
	print


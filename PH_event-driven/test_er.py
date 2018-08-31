from spreading_CR import SpreadingProcess
from timeit import default_timer
import networkx as nx
from random import sample
from numpy import inf


files = ['nwk/er10.0','nwk/er100.0','nwk/er1000.0']
rates = [0.11636463579,0.0106072115421,0.00105114984251]

nsample = 10000

for ifile in range(3):
	s0 = 0

	G = nx.convert_node_labels_to_integers(nx.read_edgelist(files[ifile]))

	sp = SpreadingProcess(list(G.edges()), rates[ifile], 1, 0)

	start = default_timer()
	for i in range(nsample):
		sources = sample(range(G.number_of_nodes()), 100)
		sp.initialize(sources, i)
		sp.evolve(inf)
		
		s0 += sp.get_Rnode_number_vector()[-1]
		sp.reset()
	stop = default_timer()
	print str(s0 / float(nsample) / G.number_of_nodes())
	print 'time per outbreak (s)', str((stop - start) / nsample)


from spreading_CR import SpreadingProcess
from timeit import default_timer
import networkx as nx
from random import sample
from numpy import inf

files = ['nwk/pow3.1e3.0','nwk/pow225.1e3.0','nwk/pow3.1e4.0','nwk/pow225.1e4.0','nwk/pow3.1e5.0','nwk/pow225.1e5.0','nwk/pow3.1e6.0','nwk/pow225.1e6.0','nwk/pow3.1e3.1','nwk/pow225.1e3.1','nwk/pow3.1e4.1','nwk/pow225.1e4.1','nwk/pow3.1e5.1','nwk/pow225.1e5.1','nwk/pow3.1e6.1','nwk/pow225.1e6.1','nwk/pow3.1e3.2','nwk/pow225.1e3.2','nwk/pow3.1e4.2','nwk/pow225.1e4.2','nwk/pow3.1e5.2','nwk/pow225.1e5.2','nwk/pow3.1e6.2','nwk/pow225.1e6.2','nwk/pow3.1e3.3','nwk/pow225.1e3.3','nwk/pow3.1e4.3','nwk/pow225.1e4.3','nwk/pow3.1e5.3','nwk/pow225.1e5.3','nwk/pow3.1e6.3','nwk/pow225.1e6.3','nwk/pow3.1e3.4','nwk/pow225.1e3.4','nwk/pow3.1e4.4','nwk/pow225.1e4.4','nwk/pow3.1e5.4','nwk/pow225.1e5.4','nwk/pow3.1e6.4','nwk/pow225.1e6.4']
rates=[0.0724553469924,0.0256593197893,0.0806131896306,0.00866408166137,0.0520902849188,0.00332485995794,0.0399700266818,0.00138069817996,0.0896913776647,0.0216845277964,0.086116982919,0.00771230136227,0.060675008325,0.00313155116966,0.0502156861189,0.00157484205454,0.0904337602871,0.0253137790935,0.0613635552542,0.00806511084875,0.0534827359826,0.00373265862608,0.0397863657255,0.0018709030077,0.111838790932,0.0241104221792,0.0820221875395,0.00834338993185,0.0613140470258,0.00373265862608,0.0433795939392,0.00166125792835,0.0675578682936,0.0190038473387,0.0655396930535,0.0101924420965,0.0532488842279,0.00403594530697,0.0457412369007,0.00154025307704]

nsample = 100000

for ifile in range(len(files)):
	s0 = 0

	G = nx.convert_node_labels_to_integers(nx.read_edgelist(files[ifile]))

	sp = SpreadingProcess(list(G.edges()), 3.0 * rates[ifile], 1, 0)

	start = default_timer()
	for i in range(nsample):
		sources = sample(range(G.number_of_nodes()), int(0.01 * G.number_of_nodes()))
		sp.initialize(sources, i)
		sp.evolve(inf)
		
		s0 += sp.get_Rnode_number_vector()[-1]
		sp.reset()
	stop = default_timer()
	print str(s0 / float(nsample) / G.number_of_nodes())
	print 'time per outbreak (s)', str((stop - start) / nsample)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate edge list for random graph models

Author: Guillaume St-Onge
"""

import os
import sys
import argparse
import numpy as np
from operator import *
import math
from numpy.random import random
from numpy.random import randint
import networkx as nx
import networkx.generators.random_graphs as gg

def output_edge_PL(w):
    n = len(w)
    rho = 1/float(sum(w))
    # sort weights, largest first
    # preserve order of weights for integer node label mapping
    order = sorted(enumerate(w),key=itemgetter(1),reverse=True)
    mapping = dict((c,uv[0]) for c,uv in enumerate(order))
    seq = [v for u,v in order]
    last=n-1
    for u in range(last):
        v = u+1
        factor = seq[u] * rho
        p = seq[v]*factor
        if p>1:
            p = 1
        while v<n and p>0:
            if p != 1:
                r = random()
                v += int(math.floor(math.log(r)/math.log(1-p)))
            if v < n:
                q = seq[v]*factor
                if q>1:
                    q = 1
                if random() < q/p:
                    print("{0} {1}".format(mapping[u],mapping[v]))
                v += 1
                p = q


def main(arguments):
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('model', help="Generative model for the random graph",
                        type=str)
    parser.add_argument('node_number', help="Number of nodes", type=int)
    parser.add_argument('-p', '--params',
                        help="Model specific parameter for the graph",
        type=float, nargs='*')
    parser.add_argument('-s', '--seed', help="Seed for the RNG", type=int,
        default=42)
    args = parser.parse_args(arguments)

    if args.model == "gnp":
        p = args.params[0]
        g = gg.fast_gnp_random_graph(args.node_number, p, args.seed)
        for e in g.edges():
            print("{0} {1}".format(e[0],e[1]))

    if args.model == "gnm":
        m = args.params[0]
        g = gg.gnm_random_graph(args.node_number, m, args.seed)
        for e in g.edges():
            print("{0} {1}".format(e[0],e[1]))

    elif args.model == "ba":
        m = int(args.params[0])
        g = gg.barabasi_albert_graph(args.node_number, m, args.seed)
        for e in g.edges():
            print("{0} {1}".format(e[0],e[1]))

    elif args.model == "PL": #random graph with power-law distribution
        kmin = args.params[0]
        exponent = args.params[1]
        kmax = np.sqrt(args.node_number)*kmin*(exponent-1.0)/(exponent-2.0)
        degree_vector = np.arange(kmin,kmax+1)
        degree_distribution = degree_vector**(-exponent)
        degree_distribution /= np.sum(degree_distribution)
        degree_distribution = np.concatenate((np.array([0]*int(kmin)),
            degree_distribution))
        cumulative_degree_distribution = np.array([
            np.sum(degree_distribution[0:i])
            for i in range(len(degree_distribution)+1)])
        #generate n expected degree from the dist
        u_vec = random(args.node_number)
        expected_degree_sequence = [np.searchsorted(cumulative_degree_distribution,
        u, side = 'right')-1 for u in u_vec]
        output_edge_PL(expected_degree_sequence)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

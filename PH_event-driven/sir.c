// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// code for SIR on networks by Petter Holme (2018)

#include "sir.h"

GLOBALS g;
NODE *n;

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// this routine does the bookkeeping for an infection event

void infect () {
	unsigned int i, me = g.heap[1], you;
	float t, now = n[me].time;

	del_root();
	n[me].heap = I_OR_R;
	// get the recovery time
	n[me].time += g.rexp[pcg_16()] * g.beta; // bcoz g.rexpr has a / g.beta factor
	g.s++;

	// go through the neighbors of the infected node . .
	for (i = 0; i < n[me].deg; i++) {
		you = n[me].nb[i];
		if (n[you].heap != I_OR_R) { // if you is S, you can be infected
			t = now + g.rexp[pcg_16()]; // get the infection time

			if ((t < n[me].time) && (t < n[you].time)) {
				n[you].time = t;
				if (n[you].heap == NONE) { // if not listed before, then extend the heap
					g.heap[++g.nheap] = you;
					n[you].heap = g.nheap;
				}
				up_heap(n[you].heap); // this works bcoz the only heap relationship that can be violated is the one between you and its parent
			}
		}
	}
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// this routine runs one SIR outbreak from a random seed node

unsigned int sir () {
	unsigned int i, source;
	
	g.s = 0;
	
	// initialize
	for (i = 0; i < g.n; i++) {
		n[i].heap = NONE;
		n[i].time = DBL_MAX; // to a large value
	}

	// get & infect the source
	for (g.nheap = 0; g.nheap < g.nsource; ) {
		source = pcg_32_bounded(g.n);
		if (n[source].heap == NONE) {
			n[source].time = 0.0;
			g.heap[++g.nheap] = source;
			n[source].heap = g.nheap;
		}
	}

	// run the outbreak
	while (g.nheap) infect();

	return g.s;
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
// main function handling input

int main (int argc, char *argv[]) {
	unsigned int i, us;
	FILE *fp;
#ifdef TIME
	struct timespec t0, t1;
#endif
	
	// just a help message
	if (argc != 5) {
		fprintf(stderr, "usage: ./sir [nwk file] [beta] [fraction of sources] [seed]\n");
		return 1;
	}

	g.state = (uint64_t) strtoull(argv[4], NULL, 10);
	
	// initialize parameters
	g.beta = atof(argv[2]);
	 
	// read network data file
	fp = fopen(argv[1], "r");
	if (!fp) {
		fprintf(stderr, "can't open '%s'\n", argv[1]);
		return 1;
	}
	read_data(fp);
	fclose(fp);

	g.nsource = (unsigned int) rint(g.n * atof(argv[3]));

	// allocating the heap (N + 1) because it's indices are 1,...,N
	g.heap = malloc((g.n + 1) * sizeof(unsigned int));

	for (i = 0; i < 0x10000; i++)
		g.rexp[i] = -log((i + 1) / (double) 0x10000) / g.beta;

   //set simulation average 
    unsigned int navg = ceil(1000000./g.n);
    double total_recovered = 0;

#ifdef TIME
	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t0);
#endif

	// run the simulations and summing for averages
	for (i = 0; i < navg; i++) {
		us = sir();
        total_recovered += us;
	}

#ifdef TIME
	clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &t1);
#endif


#ifdef TIME
    //output in microseconds
	printf("%g %g\n", 1e6 * ((t1.tv_sec - t0.tv_sec) + 1.0e-9 * (t1.tv_nsec - t0.tv_nsec)) / (2 * total_recovered), total_recovered/(g.n * navg));
#endif

	// cleaning up
	for (i = 0; i < g.n; i++) free(n[i].nb);
	free(n); free(g.heap);
	 
	return 0;
}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

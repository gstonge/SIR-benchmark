/**
* \file time_SIR.cpp
* \brief Determine the computational time for the SIR
model on networks.
* \author Guillaume St-Onge
* \version 1.0
* \date 09/02/2018
*/

#include <SpreadingProcess.hpp>
#include <io_data.hpp>
#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <vector>
#include <chrono>
#include <cmath>
#include <limits>

using namespace std;
using namespace std::chrono;
using namespace net;


int main(int argc, char const *argv[])
{
	// Get the simulation parameters from the command line
	string edge_list_path = argv[1];
	double transmission_rate = stod(argv[2]); //to be determined
	double infected_fraction = stod(argv[3]);
	unsigned int seed = atoi(argv[4]);
	double recovery_rate = 1.;
	double waning_immunity_rate = 0; //SIR

	// Initialize RNG
	RNGType gen(seed);

    // Initialize process
	std::vector<std::pair<NodeLabel, NodeLabel> > edge_list = input_edge_list(
		edge_list_path);
    SpreadingProcess sp(edge_list, transmission_rate, recovery_rate,
            waning_immunity_rate, 2);

	//determine the number of repetition to reduce variance
	size_t repetition = ceil(1000000./sp.get_size());
	double average_time_span = 0.;
    double total_recovered = 0;

    //benchmark time
    steady_clock::time_point t1 = steady_clock::now();
	for (unsigned int i = 0; i < repetition; ++i)
	{
        sp.initialize(infected_fraction,100*seed+i);
        sp.evolve(numeric_limits<int>::max());
        total_recovered += sp.get_Rnode_number();
        sp.reset();
	}
	steady_clock::time_point t2 = steady_clock::now();
	duration<double> time_span = duration_cast<duration<double>>(t2 - t1);

	average_time_span = time_span.count() / (2 * total_recovered);

	cout << 1000000*average_time_span << " " << total_recovered/(sp.get_size() * repetition) << endl; //in microseconds

	return 0;
}

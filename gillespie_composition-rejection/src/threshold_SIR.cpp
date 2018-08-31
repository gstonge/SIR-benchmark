
/**
* \file threshold_SIR.cpp
* \brief Determine the threshold for SIR dynamics
model on networks.
* \author Guillaume St-Onge
* \version 1.0
* \date 09/02/2018
*/

#include <evolution.hpp>
#include <io_data.hpp>
#include <iostream>
#include <string>
#include <cstring>
#include <sstream>
#include <vector>
#include <chrono>
#include <cmath>

using namespace std;
using namespace std::chrono;
using namespace net;


int main(int argc, char const *argv[])
{
	// Get the edge list
	string edge_list_path = argv[1];

	//Get the degree sequence and network size
	std::vector<std::pair<NodeLabel, NodeLabel> > edge_list = input_edge_list(
		edge_list_path);
	Network* temp_net_ptr = new Network(edge_list);
	size_t network_size = temp_net_ptr->size();
	vector<double> degree_sequence;
	degree_sequence.reserve(temp_net_ptr->size());
	for (int i = 0; i < temp_net_ptr->size(); i++)
	{
		degree_sequence.push_back(temp_net_ptr->degree(i));
	}
	delete temp_net_ptr;

	//determine the threshold
	double numerator = 0.;
	double denominator = 0.;
	double max_degree = 0.;
	for (int i = 0; i < degree_sequence.size(); i++)
	{
		numerator += degree_sequence[i];
		denominator += degree_sequence[i]*(degree_sequence[i]-2);
	}
	double threshold = numerator/denominator;

    cout << threshold << endl;

	return 0;
}

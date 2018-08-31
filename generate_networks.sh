# Generates the edge lists for the benchmark
#--------------------------------------------

NSAMPLE=10
EDGELIST_PATH="dat/edge_lists/"

#generate the gnm networks
MLIST="50000 150000 500000 1500000 5000000"

for M in $MLIST
do
    for SEED in $(seq 1 $NSAMPLE)
    do
        python generate_random_graph.py gnm 10000 -p $M -s $SEED > $EDGELIST_PATH/gnm_n1E4/m$M\_$SEED.txt
    done

done

#generate the power law networks
NLIST="1000 3000 10000 30000 100000 300000 1000000"

for N in $NLIST
do
    for SEED in $(seq 1 $NSAMPLE)
    do
        python generate_random_graph.py PL $N -p 3 2.25 -s $SEED > $EDGELIST_PATH/power_law_225/n$N\_$SEED.txt
        python generate_random_graph.py PL $N -p 3 3.0 -s $SEED > $EDGELIST_PATH/power_law_300/n$N\_$SEED.txt
    done
done


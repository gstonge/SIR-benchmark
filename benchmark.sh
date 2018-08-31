#comparison of the event-driven method of Petter Holme and the
#node-based (composition-rejection) approach

NSAMPLE=20
#NETWORK_TYPE_LIST="gnm_n1E4 power_law_225 power_law_300"
NETWORK_TYPE_LIST="power_law_225 power_law_300"
INFECTED_FRACTION=0.01

for NETWORK_TYPE in $NETWORK_TYPE_LIST
do
    for NETWORK in $(ls "dat/edge_lists/$NETWORK_TYPE/")
    do
        for SEED in $(seq 1 $NSAMPLE)
        do
            EDGELIST_PATH="dat/edge_lists/$NETWORK_TYPE/$NETWORK"
            #determine threshold
            THRESHOLD=$(./gillespie_composition-rejection/bin/threshold_SIR $EDGELIST_PATH)
            if [ "$NETWORK_TYPE" == "gnm_n1E4" ]
            then
                TRANSMISSION_RATE=$(echo "1.05 * $THRESHOLD" | bc)
            else
                TRANSMISSION_RATE=$(echo "3 * $THRESHOLD" | bc)
            fi
            #perform simulation for both methods
            RESULT_ED=$(./PH_event-driven/sir $EDGELIST_PATH $TRANSMISSION_RATE $INFECTED_FRACTION $SEED)
            RESULT_CR=$(./gillespie_composition-rejection/bin/time_SIR $EDGELIST_PATH $TRANSMISSION_RATE $INFECTED_FRACTION $SEED)
            echo $RESULT_ED >> "dat/SIR_results/event-driven/$NETWORK_TYPE/$NETWORK"
            echo $RESULT_CR >> "dat/SIR_results/composition-rejection/$NETWORK_TYPE/$NETWORK"
        done
    done
done

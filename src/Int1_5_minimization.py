from src import Int1_5_algorithms as Algo
from src import Int1_5_determinization as Det


def display_partition(partition, step):
    """
        should display the repartition e.g :
        Partition number 0:
        ---> A: 0, 3, 9
        ---> B: 1, 2, ...
    """
    print("Here is the partition θ[" + str(step) + "]: ", partition)
    for i in range(len(partition)):
        print("---> " + chr(65 + i) + ":", end=" ")
        for j in range(len(partition[i])):
            print(partition[i][j], end=", ")
        print()


def detect_pattern(partition: list, index_sub_partition: int, automaton: dict):
    """
        Detects the patterns of the destinations in ONE SUBSET of the partition
        Args : The partition, the index of the considered sub-partition, the original automaton
        Returns : A list of sublists which are the patterns of each sub-partitions e.g. [[1,0,2], [0,0,2]]
    """
    pattern_of_subset = []
    letters = automaton['alphabet']
    for i in range(len(partition[index_sub_partition])):
        pattern_of_state = []
        for j in range(len(letters)):
            # how to get the destination of this transition
            dest = [t['to'] for t in automaton['transitions'] if t['from'] == partition[index_sub_partition][i]
                    and t['input'] == letters[j]]
            # now get the index of the sublist in which dest is
            dest_index = [k for k in range(len(partition)) if dest[0] in partition[k]]
            # now insert that index in the list pattern_of_state e.g. [1,3,6]
            pattern_of_state.append(dest_index[0])
        # pattern_of_subset will have the sublists of the pattern of each state
        pattern_of_subset.append(pattern_of_state)
    return pattern_of_subset


def display_transitions(partition: list, automaton: dict, pattern_of_partition: list, step: int):
    """
        Displays the transitions of the states according to the sub-partitions in the given partition
        Args : The considered partition, the original automaton, the list of patterns of the partition,
            the step (number of times we calculate a new partition
        Returns : None
    """
    print(f"Here are the transitions of each sub_partition according to θ[{step}]:")
    letters = automaton["alphabet"]
    # First line with the alphabet
    print(end="|{:^10}".format(""))
    for letter in letters:
        print(end="|{:^10}".format(letter))
    print("|")

    for i in range(len(partition)):
        print("-" * 11 * (len(letters) + 1))
        for j in range(len(partition[i])):
            print(end="|{:^10}".format(partition[i][j]))
            for k in range(len(letters)):
                print(end="|{:^10}".format(chr(65 + pattern_of_partition[i][j][k])))
            print("|")
    print("\n")


def repartition(partition: list, index: int, automaton: dict):
    """
        Given the sub-partition of a partition => it will divide it or not according to the patterns of the states
        Args : The partition, the index of the sub-partition to be analysed, the original automaton
        Returns : A list (either [partition[i]] itself, or a list w. sublists)
    """
    if len(partition[index]) == 1:
        pattern_of_subset = detect_pattern(partition, index, automaton)
        return [partition[index]], pattern_of_subset

    pattern_of_subset = detect_pattern(partition, index, automaton)
    final_sub_partition = [[partition[index][0]]]

    for i in range(1, len(partition[index])):
        j_pattern = 0
        j_sub_part = 0
        checked_pattern = []
        while j_sub_part < len(final_sub_partition) and (pattern_of_subset[i] != pattern_of_subset[j_pattern]):
            if pattern_of_subset[j_pattern] not in checked_pattern:
                checked_pattern.append(pattern_of_subset[j_pattern])
                j_sub_part += 1
            j_pattern += 1

        if j_sub_part < len(final_sub_partition):
            final_sub_partition[j_sub_part].append(partition[index][i])
        else:
            final_sub_partition.append([partition[index][i]])
    if len(final_sub_partition) == 1:
        return [partition[index]], pattern_of_subset
    else:
        return final_sub_partition, pattern_of_subset


def minimization(cdfa: dict):
    """
        Minimizes the given automaton (that should already be a CDFA)
        Args : the CDFA
        Returns : Minimization_Possible (bool) Already_Minimal (bool), mcdfa (dict), partition (list of sub-partitions)
    """
    print("We have to minimize this automaton :")
    Algo.display_automaton(cdfa)

    print("\n---STARTING MINIMIZATION---")
    step = -1
    partition = [cdfa['finalStates'], [state for state in cdfa['states'] if state not in cdfa['finalStates']]]
    partition_state = [False, False]
    pattern_of_partition = []
    # while there are sub-partitions to analyze, we do all the things below
    while False in partition_state:
        step += 1
        # First of all - display the partition
        # Must detect the pattern in partition in order to display the table transition before analysing them
        display_partition(partition, step)
        for index_sub_partition in range(len(partition)):
            pattern_of_subset = detect_pattern(partition, index_sub_partition, cdfa)
            pattern_of_partition.append(pattern_of_subset)
        display_transitions(partition, cdfa, pattern_of_partition, step)

        temp_partition = []
        temp_partition_state = []
        temp_pattern_of_partition = []
        for i in range(len(partition)):
            if not partition_state[i]:
                sub_partition_i, pattern_of_subset = repartition(partition, i, cdfa)
                if partition[i] == sub_partition_i[0]:
                    temp_partition.append(sub_partition_i[0])
                    temp_partition_state.append(True)
                else:
                    for j in range(len(sub_partition_i)):
                        temp_partition.append(sub_partition_i[j])
                        temp_partition_state.append(False)
            else:
                pattern_of_subset = detect_pattern(partition, i, cdfa)
                temp_partition.append(partition[i])
                temp_partition_state.append(True)
            temp_pattern_of_partition.append(pattern_of_subset)

        partition = temp_partition
        partition_state = temp_partition_state
        pattern_of_partition = temp_pattern_of_partition

    # Verifying if the automaton was already
    if len(partition) == len(cdfa['states']):
        print(f"We have the same number of states, so, the automaton #{cdfa['id']} was already minimal !")
        return True, cdfa, None

    # construct the new cdfa (create the dictionary that will be returned - using pattern of partition)
    mcdfa = {"id": cdfa["id"]+"-MINIMIZED", "states":[chr(65+i) for i in range(len(partition))],
             "alphabet": cdfa["alphabet"],
             "initialStates": cdfa["initialStates"],
             "finalStates": [],
             "transitions": []}
    # must define the final states of mcdfa
    for i in range(len(partition)):
        for j in range(len(partition[i])):
            if partition[i][j] in cdfa["finalStates"] and chr(65+i) not in mcdfa["finalStates"]:
                mcdfa["finalStates"].append(chr(65+i))
    # must define all the transitions
    for i in range(len(pattern_of_partition)):
        for j in range(len(pattern_of_partition[i][0])):
            transition = {"from": chr(65+i), "input": mcdfa["alphabet"][j], "to": chr(65+pattern_of_partition[i][0][j])}
            mcdfa["transitions"].append(transition)
    return False, mcdfa, partition


def display_minimal_automaton(already_minimal: bool, mcdfa: dict, partition):
    if already_minimal:
        print("No changes is needed !: ")
        Algo.display_automaton(mcdfa)
    else:
        print("MINIMAL AUTOMATON: ")
        display_partition(partition, "final")
        Algo.display_automaton(mcdfa)

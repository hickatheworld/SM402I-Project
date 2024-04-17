import os
import json


# Parses the automata data from a given file according to it's ID
def get_automaton_by_id(automaton_id, filename):
    """
        Args:
            ID : The id of the automaton filepath: Path of the file to parse.
        Returns:
            A dictionary for the automata who's ID was given
    """
    with open(filename, "r") as file:
        data = json.load(file)
    for automaton in data["automatas"]:
        if automaton["id"] == str(automaton_id):  # IDs are strings in the JSON
            return {
                "id": automaton["id"],
                "states": automaton["states"],
                "alphabet": automaton["alphabet"],
                "transitions": [
                    {"from": transition[0], "input": transition[1], "to": transition[2]}
                    for transition in automaton["transitions"]
                ],
                "initialStates": automaton["initialStates"],
                "finalStates": automaton["finalStates"]
            }

    # If the automaton with the given ID is not found
    return None


# Saves given automaton dictionary to file.
def save_automaton(automaton):
    """
    Args:
        automaton: automaton to save
    Returns :
        nothing
    """
    # converts dictionary to a json formatted string
    json_str = json.dumps(automaton)
    with open(f"INT1-5-{automaton['id']}.txt", "w") as file:
        file.write(json_str)


# Displays given automaton
def display_automaton(automaton):
    """
    Args:
        automaton: Automaton to display as a table
    Returns:
        nothing
    """

    print(f"Automaton #{automaton['id']}")
    if "E" in [transition["input"] for transition in automaton["transitions"]]:
        letters = automaton["alphabet"] + ["E"]
    else:
        letters = automaton["alphabet"]
    # First line with the alphabet
    print(end="|{:^8}".format(""))
    print(end="|{:^10}".format(""))
    for letter in letters:
        print(end="|{:^10}".format(letter))
    print(end="|")

    for state in automaton["states"]:
        # First column of each line => is the state an entry//terminal state ?
        if state in automaton["initialStates"] and state in automaton["finalStates"]:
            print("\n", end="|{:^8}".format("<->"))
        elif state in automaton["initialStates"]:
            print("\n", end="|{:^8}".format("->"))
        elif state in automaton["finalStates"]:
            print("\n", end="|{:^8}".format("<-"))
        else:
            print("\n", end="|        ")
        # Second column of each line => display the state
        print(end="|{:^10}".format(state))

        # Other columns of each line => destination states by each letter
        for letter in letters :
            # list_dest will consider all transitions from given state with given input, but it only takes the DESTINATIONS
            list_dest = [transition['to'] for transition in automaton['transitions'] if transition['from'] == state and transition['input'] == letter]
            # if there is no destination then bruh --
            if not list_dest:
                print(end="|{:^10}".format("--"))
            # else we create the string such as 0,1,2 (it won't necessarily be in ascending order)
            else:
                str_dest = list_dest[0]
                i = 1
                while i<len(list_dest) :
                    str_dest += f",{list_dest[i]}"
                    i +=1
                print(end="|{:^10}".format(str_dest))
        print("|")


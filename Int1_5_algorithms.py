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
        automaton: Automaton to display
    Returns:
        nothing
    """

    print(f"Automaton #{automaton['id']}")
    print(end="|        " * 2)
    for letter in automaton['alphabet']:
        print(end="|    {}    " .format(letter))
    print(end="|")
    # above it's ok - first line$
    print("\n", end="----------"*(len(automaton['alphabet'])+2)) # limit of first line


    for state in automaton["states"]:
        if state in automaton["initialStates"] and state in automaton["finalStates"]:
            print("\n", end="|  <->  ")
        elif state in automaton["initialStates"]:
            print("\n", end="|   ->   ")
        elif state in automaton["finalStates"]:
            print("\n", end="|   <-   ")
        else:
            print("\n", end="|        ")
        print(end="|    {}    ".format(state))
        #a remplir - transitions

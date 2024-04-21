import os
import json


def get_automaton_by_id(automaton_id: int, filename: str):
    """
        Args:
            ID : The id of the automaton filepath: Path of the file to parse.
        Returns:
            A dictionary for the automata whose ID was given
    """
    with open(filename, "r") as file:
        data = json.load(file)
    for automaton in data["automatas"]:
        # IDs are strings in the JSON
        if automaton["id"] == str(automaton_id):
            # Returning a dictionary with renamed keys for clarity
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


def save_automaton(automaton: dict):
    """
    Saves the given automaton to a text file.
    Args:
        automaton: automaton to save
    Returns :
        nothing
    """
    # Converts dictionary to a json formatted string
    # Adding indent=4 allows for more beautiful txt files
    json_str = json.dumps(automaton, separators=(",", ":"), indent=4)
    # Creating a folder for modified automata
    os.makedirs("src/automata/modified", exist_ok=True)
    # Changing to this folder to save them into it
    os.chdir("src/automata/modified")
    with open(f"INT1-5-{automaton['id']}.txt", "w") as file:
        file.write(json_str)


def display_automaton(automaton: dict):
    """
    Displays the given automaton.
    Args:
        automaton: automaton to display as a table
    Returns:
        nothing
    """
    print(f"Automaton #{automaton['id']}") 
    if "E" in [transition["input"] for transition in automaton["transitions"]]: # "E" is the symbol for epsilon
        letters = automaton["alphabet"] + ["E"]
    else:
        letters = automaton["alphabet"]

    #                                    DISPLAYING HEADER LINE                                       #
    print(end="|{:^8}".format(""))
    print(end="|{:^10}".format(""))
    for letter in letters:
        print(end="|{:^10}".format(letter))
    print(end="|")

    # DISPLAYING TABLE BODY
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
        for letter in letters:
            # list_dest will consider all transitions from given state with given input, but it only takes the DESTINATIONS
            list_dest = [transition['to'] for transition in automaton['transitions'] if transition['from'] == state and transition['input'] == letter]
            # If there is no destination then "--"
            if not list_dest:
                print(end="|{:^10}".format("--"))
            # Else we create the string such as 0,1,2 (it won't necessarily be in ascending order)
            else:
                str_dest = list_dest[0]
                i = 1
                while i<len(list_dest) :
                    str_dest += f",{list_dest[i]}"
                    i += 1
                print(end="|{:^10}".format(str_dest))
        print("|", end="")
    print("\n")


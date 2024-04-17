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
                "initialState": automaton["initialState"],
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




def display_automaton(automaton: dict) -> None:
    """
    WIP. Displays given automaton

    Args:
        automaton: Automaton to display
    """

    print(f"Automaton #{automaton['id']}")

    for letter in automaton['alphabet']:
        print(letter, end=' '*4)
    print()
    for state in automaton['states']:
        line = ''
        line +='I' if state in automaton['initialStates'] else ' '
        line +='F' if state in automaton['finalStates'] else ' '
        line +=' '
        print(f'{line} {state}',end=' '*4)
        for symbol in automaton['alphabet']:
            transitions = ''
            for t in automaton['transitions']:
                if t[0]==state and t[1]==symbol:
                    transitions+=t[2] + ','
            transitions = transitions[:-1]
            if transitions=='':
                transitions = '-'
            print(transitions,end=' '*4)
        print()
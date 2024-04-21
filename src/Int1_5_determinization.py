from typing import List

def is_deterministic(automaton: dict) -> bool:
    """
    Checks if the automaton is deterministic.
    Args: The automaton to analyse
    Returns: True if deterministic, False otherwise
    """
    # Check if there are more than one entry state
    if len(automaton["initialStates"]) > 1:
        return False

    # Checking for multiple transitions from the same state with the same labelled transition
    dico_transitions = {}
    for transition in automaton['transitions']:
        key = (transition['from'], transition['input'])
        if key in dico_transitions:
            # If the key already exists, then we have two outgoing labels from the same state, hence not deterministic
            return False
        else:
            # Otherwise we add it to the transition dictionary
            dico_transitions[key] = transition['to']

    # All checks pass so the automaton is deterministic
    return True

def is_complete(automaton: dict) -> bool:
    """
    Checks if the automaton is complete.
    Args: The automaton to analyse
    Returns: True if complete, False otherwise
    """
    language = []
    for transition in automaton['transitions']:
        language.append(transition['input'])

    # Checking if all transition from each state are labelled with all symbols of the language
    for state in automaton['states']:
        for symbol in language:
            found = False
            for transition in automaton['transitions']:
                if transition['from'] == state and transition['input'] == symbol:
                    found = True
                    break
            if not found:
                return False

    # All checks pass so the automaton is complete
    return True

def completion(automaton: dict) -> dict:
    """
    Completes the automaton by adding missing transitions.
    Args: The automaton to complete
    Returns: The completed automaton
    """
    language = []
    for transition in automaton['transitions']:
        language.append(transition['input'])

    # List for completed transitions
    completed_transitions = automaton['transitions'][:]

    # Checking if all transition from each state are labelled with all symbols of the language (again)
    for state in automaton['states']:
        for symbol in language:
            found = False
            for transition in automaton['transitions']:
                if transition['from'] == state and transition['input'] == symbol:
                    found = True
                    break
            if not found:
                # If a transition is not found for a symbol, we add it to a bin state we denote 'P'
                completed_transitions.append({'from': state, 'to': 'P', 'input': symbol})

    # Adding the bin state if it doesn't exist
    if 'P' not in automaton['states']:
        automaton['states'].append('P')

    # Returning the completed automaton
    return {'states': automaton['states'], 'alphabet': automaton['alphabet'], 'transitions': completed_transitions, 'initialStates': automaton['initialStates'], 'finalStates': automaton['finalStates']}

def determinize(automaton: dict) -> dict:
    """
    Determinizes an automaton 
    ! Warning ! - only works with non determinzed automata
    Args : the automaton given as a dict
    Returns : the determinized automaton
    """

    # Reduce to only one initial state if necessary 
    initialStates = automaton["initialStates"]
    if len(initialStates) > 1:  
        print("There is more than one initial state - Merging them...")   # Logging 
        initialStates = associate_states_transitions(automaton, initialStates)

        new_initial_statedict = create_composite_from_list_of_dicts(initialStates)  # is weird but this returns a dict
        print("Done merging.")   # Logging
    else:
        initialStates = associate_states_transitions(automaton, initialStates)
        new_initial_statedict = create_composite_from_list_of_dicts(initialStates)  # is weird but this returns a dict
        print("There is only one initial state. - No need to merge.") # Logging
    
    # Apply the determinazation algorithm
    states_to_study = [new_initial_statedict]       # TODO: make sure initial_state here is dict[str, dict(str, str, str)]
    # We should write a function to copy automatons with parameters

  
    
    DFA = {
        "id" : automaton["id"]+"-DETERMINIZED",
        "states" : [new_initial_statedict["state"]],
        "alphabet" : automaton["alphabet"],
        "transitions" : [],  # empty for now
        "initialStates" : [new_initial_statedict["state"]],
        "finalStates" : []  # empty for now
    }
    while states_to_study != []:
        studying = states_to_study[0]

        for symbol in automaton["alphabet"]:
            arrival_states = find_arrival_states_by_symbol_from_states(studying["composing_states"], studying["transitions"], symbol)
            arrival_states = associate_states_transitions(automaton, arrival_states)
            new_state = create_composite_from_list_of_dicts(arrival_states)

            # This test can be factorized in : newstate not in (A union B)
            if new_state not in states_to_study and new_state["state"] not in DFA["states"]:
                if new_state != "":
                    states_to_study.append(new_state)
            
            # Update the DFA - add transitions
            
            DFA["transitions"].append({"from":states_to_study[0]["state"], "input":symbol, "to":new_state["state"]})
            
            # Tweak the finalStates list
            if states_to_study[0]["state"] not in DFA["finalStates"] and composed_is_final(automaton, states_to_study[0]["state"]):
                
                DFA["finalStates"].append(states_to_study[0]["state"])

            # update the DFA - add states
            if new_state["state"] not in DFA["states"]:
                if new_state["state"] != "":
                    DFA["states"].append(new_state["state"])
        states_to_study.pop(0)
        # print(f"we done studying {done_with}. Still left : {states_to_study}")
        
    print("done with determinizing... oof !\n")

    return DFA


def associate_states_transitions(automaton: dict, states: List[str]) -> List[dict]:
    """
    Create a list of dictionnaries matching states with their associated transitions

    Args: The dictionnary containing all the info
    Returns: The list of matching states-transitions
    """
    list_of_dict = []
    for state in states:
        dict_state = {"state": state}
        dict_state["transitions"] = []
        for transition in automaton["transitions"]:
            if transition["from"] == state:
                dict_state["transitions"].append(transition)
        list_of_dict.append(dict_state)

    return list_of_dict

def find_arrival_states_by_symbol_from_states(states:List[str], transitions:List[dict], symbol: str) -> List[dict[str, dict[str, str, str]]]:
    """
    Find the arrival states by symbol from a given state in a transition table.

    Args:
        state: The current state.
        transition: The transition table.
        symbol: The symbol to search for.

    Returns:
        A list of dictionaries representing the arrival states for the given symbol from the given state.
        Each dictionary contains the following keys:
            - 'state': The arrival state.
            - 'symbol': The symbol that leads to the arrival state.
            - 'next_state': The next state after transitioning from the current state using the given symbol.
    """
    arrival_state = []
    scanned = []
    for state in states:
        for transition in transitions:  
            if transition["from"] == state:
                if transition["input"] == symbol:
                    if transition not in scanned:   # avoid infinite looping 
                        scanned.append(transition)
                        arrival_state.append(transition["to"])
    return arrival_state
    
def create_composite_from_list_of_dicts(states: List[dict[str, dict[str, str, str]]]) -> dict[str, dict[str, str, str]]:
    """
    Create a composite state from a list of states.

    Args:
        states (List[dict[str, dict[str, str, str]]]): A list of dictionaries representing the states you want to merge.

    Returns:
        dict[str, dict[str, str, str]]: A composite state and its transition table in the dictionnary form.

    """
    composite_state = {
        "state": "",
        "transitions": [],
        "composing_states" : []
    }
    
    for state in states:
        if not state["state"] in composite_state["state"]:
            composite_state["state"] += "." + state["state"]
        composite_state["composing_states"].append(state["state"])
        for transition in state["transitions"]:
            composite_state["transitions"].append(transition)

    # remove trailing "." that may have slipped in the new composite state name
    composite_state["state"] = composite_state["state"].strip(".")
    
    return composite_state



def composed_is_final(automaton:dict, composite_state: str) -> bool:

    list_of_states_composing = composite_state.split(".")
    
    
    for state in list_of_states_composing:
        if state in automaton["finalStates"]:
            return True

    return False


def determinization_and_completion_automaton(automaton: dict) ->dict:
    """
    Merges the completion and determinize funtions into one
    Args: The undeterministic and uncomplete automaton
    Returns: The deterministic and complete automaton
    """
    # Calling the completion function upon the automaton
    completed = completion(automaton)
    # Calling the determinize function over that same completed automaton
    determinized = determinize(completed)
    return determinized



# TODO : Remove this testing part
if __name__ == "__main__":

    from Int1_5_algorithms import get_automaton_by_id
    from Int1_5_algorithms import display_automaton




    for i in range(1, 45):
    # for i in range(29, 30):
        myautomaton = get_automaton_by_id(str(i), "src/automata/automatas.json")
        print(f"i : {i}-", is_deterministic(myautomaton))

        if not is_deterministic(myautomaton):
            if i == 29:
                import json
                with open("temp.txt", 'w') as tmpfile1:
                    tmpfile1.write(json.dumps(determinize(myautomaton), separators=(",", ":"), indent=4))


            display_automaton(determinize(myautomaton))

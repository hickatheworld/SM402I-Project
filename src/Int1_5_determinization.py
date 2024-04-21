from typing import List
import copy
def is_deterministic(automaton: dict) -> bool:
    """
    Checks if the automaton is deterministic.
    Args: The automaton to analyse
    Returns: True if deterministic, False otherwise
    """
    # Checking for epsilon transitions
    for transition in automaton['transitions']:
        if transition['input'] == 'E':
            return False
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
    copied_automata = copy.deepcopy(automaton)   # avoid any pass by reference
    automaton = copied_automata
    


    # Create a list that will be completed with transitions
    completed_transitions = automaton['transitions']

    # Checking if all transition from each state are labelled with all symbols of the language (again)
    for state in automaton['states']:
        for symbol in automaton["alphabet"]:
            found = False
            for transition in completed_transitions:
                if transition['from'] == state and transition['input'] == symbol:
                    found = True
                    break
            if not found:
                # If a transition is not found for a symbol, we add it to a bin state we denote 'P'
                completed_transitions.append({'from': state, 'to': 'P', 'input': symbol})

    # Adding the bin state if it doesn't exist
    if 'P' not in automaton['states']:
        automaton['states'].append('P')
        # and complete this bin state
        for symbol in automaton["alphabet"]:
            automaton["transitions"].append({"from": "P", "to": "P", "input": symbol})

    # Creating the completed automaton name
    automaton["id"] += "-COMPLETED"

    # Returning the completed automaton
    return {
        'id': automaton["id"],
        'states': automaton['states'],
        'alphabet': automaton['alphabet'],
        'transitions': completed_transitions,
        'initialStates': automaton['initialStates'],
        'finalStates': automaton['finalStates']
        }

def determinize(automaton: dict) -> dict:
    """
    Determinizes an automaton 
    Args: the automaton given as a dict
    Returns: the determinized automaton
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
    states_to_study = [new_initial_statedict]
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

def determinize_async(automaton: dict) -> dict:
    """
    Determinizes an asynchronous automaton, using epsilon closures.
    Args: The automaton to determinize
    Returns: The determinized automaton
    """
    eclosures = {}
    for state in automaton['states']:
        # Each state has an epsilon closure that contains itself
        eclosures[state] = [state]
        for transition in automaton['transitions']:
            # Any transition from this state by epsilon is added to the epsilon closure
            if transition['from'] == state and transition['input'] == 'E':
                eclosures[state].append(transition['to'])
                # But we also have to retroactively reperctute 
                # this to all epsilon-closures that include this state
                for i in eclosures:
                    ec = eclosures[i]
                    if state in ec and transition['to'] not in ec:
                        ec.append(transition['to'])
    # Sorting each epsilon closure for readability
    eclosures = {k: sorted(v) for k, v in eclosures.items()}
    # Now we can determinize the automaton
    dfa = {'id': automaton['id'] + '-DETERMINIZED'}
    dfa['alphabet'] = automaton['alphabet'].copy()
    original_initial = automaton['initialStates'][0] # We know there is only one initial state
    initial_state = original_initial
    dfa['initialStates'] = initial_state 
    composite_states = [[initial_state]]
    transitions = []
    i = 0
    while i < len(composite_states): # Since we are appending to this list in the loop, we can't use a for loop
        states = composite_states[i]
        for letter in dfa['alphabet']:
            to = []
            for state in states:
                for s in eclosures[state]:
                    for transition in automaton['transitions']:
                        if transition['from'] == s and transition['input'] == letter:
                            to.append(transition['to'])
            to = sorted(list(set(to))) # Remove duplicates and sort
            transitions.append({'from': states, 'input': letter, 'to': to})
            if to not in composite_states and to != []:
                composite_states.append(to)
        i += 1 
    dfa['states'] = composite_states
    dfa['transitions'] = transitions
    dfa['finalStates'] = [state for state in composite_states if any(any(e in automaton['finalStates'] for e in eclosures[s]) for s in state)]
    # Now, we have to convert composite states to strings in initialStates, finalStates, states and transitions
    dfa['initialStates'] = ['.'.join(eclosures[dfa['initialStates'][0]])]
    for i in range(len(dfa['states'])):
        states = []
        composite = dfa['states'][i]
        for s in composite:
            states+= eclosures[s]
        dfa['states'][i] = '.'.join(sorted(list(set(states))))
    for i in range(len(dfa['finalStates'])):
        states = []
        composite = dfa['finalStates'][i]
        for s in composite:
            states+= eclosures[s]
        dfa['finalStates'][i] = '.'.join(sorted(list(set(states))))
    for i in range(len(dfa['transitions'])):
        transition = dfa['transitions'][i]
        from_states = []
        for s in transition['from']:
            from_states+= eclosures[s]
        transition['from'] = '.'.join(sorted(list(set(from_states))))
        to_states = []
        for s in transition['to']:
            to_states+= eclosures[s]
        transition['to'] = '.'.join(sorted(list(set(to_states))))
    print(dfa)
    return dfa


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

    is_async = False
    for transition in automaton['transitions']:
        if transition['input'] == 'E':
            is_async = True
            break
    # Calling the determinize function over that same completed automaton
    determinized = determinize(completed) if not is_async else determinize_async(completed)
    
    return determinized

if __name__ == "__main__":
    import json
    automata = json.load(open("src/automata/automata.json"))
    determinize_async(automata[30])
    
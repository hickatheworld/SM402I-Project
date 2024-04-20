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
    completed_transitions = automaton['transitions'].copy()

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
    return {
        id: f'{automaton["id"]}_completed',
        'states': automaton['states'], 
        'alphabet': automaton['alphabet'], 
        'transitions': completed_transitions, 
        'initialStates': automaton['initialStates'], 
        'finalStates': automaton['finalStates']
        }



def determinize(automaton: dict) -> dict:
    """
    Determinizes an automaton
    Args : the automaton given as a dict
    Returns : the determinized automaton
    """
    if is_deterministic(automaton):
        return automaton
    
    else:
        # Reduce to only one initial state if necessary 
        initialStates = automaton["initialStates"]
        if len(initialStates) > 1:  
            print("There is more than one initial state - Merging them...")   # Logging 
            new_initial_state = merge_states(automaton, initialStates)
            print("Done merging.")   # Logging
        else:
            print("There is only one initial state. - No need to merge.") # Logging
        
        # Apply the determinazation algorithm
        states_to_study = [new_initial_state]       # TODO: make sure initial_state here is dict[str, dict(str, str, str)]

        # We should write a function to create automatons with parameters
        DFA = {
            "id" : automaton["id"] + '_determinized',
            "states" : [new_initial_state],
            "transitions" : [],  # empty for now
            "initialStates" : [new_initial_state],
            "finalStates" : []  # empty for now
        }

        while states_to_study != []:
            studying = states_to_study[0]
            for symbol in automaton["alphabet"]:
                arrival_states = find_arrival_states_by_symbol_from_state(studying["trans"], studying["state"], symbol)
                new_state = create_composite_from_list_of_dicts(arrival_states)

                # This test can be factorized in : newstate not in (A union B)
                if new_state not in states_to_study and new_state not in DFA["states"] :
                        states_to_study.enqueue(new_state)
                
                # Update the DFA - add transitions
                DFA["transitions"].append({"from":states_to_study[0]["state"], "input":symbol, "to":new_state["state"]})
                
                # Tweak the finalStates list
                if states_to_study[0]["state"] not in DFA["finalStates"]:
                    DFA["finalStates"].append(states_to_study[0]["state"])

                if new_state not in DFA["states"]:
                    DFA["states"].append(new_state["state"])

            # Log it for debugging bruh
            done_with = states_to_study.dequeue()
            print(f"we done studying {done_with}. Still left : {states_to_study}")
            
        print("done with determinizing... oof !\n")
        return DFA

def find_arrival_states_by_symbol_from_state(state, transition, symbol) -> List[dict[str, dict[str, str, str]]]:
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
    
    
    
    return
    
def create_composite_from_list_of_dicts(states: List[dict[str, dict[str, str, str]]]) -> dict[str, dict[str, str, str]]:
    """
    Create a composite state from a list of states.

    Args:
        states (List[dict[str, dict[str, str, str]]]): A list of dictionaries representing the states you want to merge.

    Returns:
        dict[str, dict[str, str, str]]: A composite state and its transition table in the dictionnary form.

    """
    # actually up there that function is just joining the str for the names and the dicts for the transi lol 
    return None


def merge_states(original_automaton: dict,  states_to_merge: List[str]):
    """
        Merges the states in a given list
        Args: The automaton to determinize & the states to merge
        Returns: The dictionary with the merged_states & list of new_transitions
    """
    merged_states = states_to_merge


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




def is_deterministic(automaton: dict) -> bool:
    """
    Checks if the automaton is deterministic.

    Args: The automaton to analyse
    Returns: True if deterministic, False otherwise
    """
    # checking for epsilon transitions
    for transition in automaton['transitions']:
        if transition['input'] == 'E':
            return False

    # checking for multiple transitions from the same state with the same labelled transition
    dico_transitions = {}
    for transition in automaton['transitions']:
        key = (transition['from'], transition['input'])
        if key in dico_transitions:
            # if key already exists, then two outgoing labels from the same state, so not deterministic
            return False
        else:
            # otherwise add to transition dictionary
            dico_transitions[key] = transition['to']

    # all checks pass so the automaton is deterministic
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

    # checking if all transition from each state are labelled with all symbols of the language
    for state in automaton['states']:
        for symbol in language:
            found = False
            for transition in automaton['transitions']:
                if transition['from'] == state and transition['input'] == symbol:
                    found = True
                    break
            if not found:
                return False

    # all checks pass so the automaton is complete
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

    # list for completed transitions
    completed_transitions = automaton['transitions'][:]

    # checking if all transition from each state are labelled with all symbols of the language (again)
    for state in automaton['states']:
        for symbol in language:
            found = False
            for transition in automaton['transitions']:
                if transition['from'] == state and transition['input'] == symbol:
                    found = True
                    break
            if not found:
                # if a transition is not found for a symbol, add one to a bin state we denote 'P'
                completed_transitions.append({'from': state, 'to': 'P', 'input': symbol})

    # adding the bin state if it doesn't exist
    if 'P' not in automaton['states']:
        automaton['states'].append('P')

    # returning the completed automaton
    return {'states': automaton['states'], 'alphabet': automaton['alphabet'], 'transitions': completed_transitions, 'initial_state': automaton['initial_state'], 'accepting_states': automaton['accepting_states']}



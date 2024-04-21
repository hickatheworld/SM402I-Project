def is_standard(automaton: dict) -> bool:
    """
    Tells whether the given automaton is a Standard Finite Automaton.
    
    Args:
        automaton: The automaton to analyse.
    Returns:
        Whether the automaton is standard.
    """
    # Condition 1. A standard automaton has only one initial state.
    if len(automaton['initialStates']) != 1:
        return 'multiple_initial_states'
    initial_state = automaton['initialStates'][0]
    # Condition 2. A standard automaton can't have any transition arriving at that unique entry.
    for transition in automaton['transitions']:
        if transition['to'] == initial_state:
            return 'transition_to_entry'
    return 'standard'

def standardize(automaton: dict) -> dict:
    """
    Turns the given automaton into a Standard Finite Autmaton, if necessary.
    
    Args:
        automaton: The automaton to standardize
    Returns:
        The standardized automaton.
    """
    if is_standard(automaton):
        return automaton
    sfa = dict() # We construct a whole new standardized automaton.
    sfa['id'] = automaton['id'] + '_SFA'

    # We must make sure to shallow copy data from the base automaton
    # to avoid any alteration to it when interacting with the newly constructed SFA.
    # Note: The copy method of dict does not perform this operation on its values, hence we do it manually.
    sfa['alphabet'] = automaton['alphabet'].copy() # The new SFA has the same alphabet as the base automaton
    # Step 1 of standardization: Create a new entry state. 
    entry = 'I' if 'I' not in automaton['states'] else 'SFA_ENTRY' # Just making sure we don't override any existing state.
    sfa['initialStates'] = [entry]
    sfa['states'] = automaton['states'].copy() + [entry]
    sfa['finalStates'] = automaton['finalStates'].copy()

    # If any initial state of the base automaton is a final state, the new entry state must be final as well.
    if any(i in automaton['finalStates'] for i in automaton['initialStates']):
        sfa['finalStates'].append(entry)

    # The constructed SFA has all the transitions from the base automaton
    sfa['transitions'] = automaton['transitions'].copy()

    # And the new entry state I copies the transition of the previous initial states.
    sfa['transitions']+= [ {'from': entry, 'input': t['input'], 'to': t['to'] } 
                          for t in automaton['transitions'] 
                          if t['from'] in automaton['initialStates']]
    return sfa
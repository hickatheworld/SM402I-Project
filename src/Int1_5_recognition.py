
def recognize_word(word: str, automaton: dict) -> bool:
    """
    Tests if a word is recognized by the given automaton.
    Args:
        word: the requested word which we want to compare to the automaton's language
        automaton: the automaton we want to compare the language of to the given word
    Returns:
        Whether the word is recognized by the automaton
    """
    current_states = set(automaton['initialStates'])
    # Add states reachable through epsilon transitions from initial states
    current_states |= epsilon_closure(current_states, automaton['transitions'])

    # Iterate through each letter in the word
    for letter in word:
        next_states = set()
        # Iterate through each transition in the automaton's transitions
        for transition in automaton['transitions']:
            # Checking if the transition's 'from' state is in current states AND if the transition's input matches the current letter
            if transition['from'] in current_states and transition['input'] == letter:
                # If the conditions are met we add the 'to' state of the current transition to next states
                next_states.add(transition['to'])
        # Add states reachable through epsilon transitions from next states
        next_states |= epsilon_closure(next_states, automaton['transitions'])
        # If no transition is found for the current letter then the word doesn't exist in the automaton
        if not next_states:
            return False
        current_states = next_states
    # If any of the last states is a final state then the word is recognized
    return any(state in automaton['finalStates'] for state in current_states)

def epsilon_closure(states: set, transitions: list) -> set:
    """
    Returns the epsilon closure of a set of states.
    Args:
        states: the set of states for which to find the epsilon closure
        transitions: the list of transitions of the automaton
    Returns:
        The epsilon closure of the set of states
    """
    # Start with the initial set of states
    closure = set(states)
    # Keep looping until no new states can be added to the closure
    while True:
        # Find all states that can be reached from the current closure through an epsilon transition
        new_states = set(state['to'] for state in transitions if state['from'] in closure and state['input'] == 'E')
        # Add these new states to the closure
        new_states |= closure
        # If no new states were added in this iteration, we have found the complete epsilon closure
        if closure == new_states:
            return closure
        # Otherwise, continue with the new closure in the next iteration
        closure = new_states
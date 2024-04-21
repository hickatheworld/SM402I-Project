
def recognize_word(word: str, automaton: dict) -> bool:
    """
    Tests if a word is recognized by the given automaton.
    Args:
        word: the requested word which we want to compare to the automaton's language
        automaton: the automaton we want to compare the language of to the given word
    Returns:
        Whether the word is recognized by the automaton
    """
    current_state = automaton['initialStates'][0]
    # Iterate through each letter in the word
    for letter in word:
        next_state = None
        # Iterate through each transition in the automaton's transitions
        for transition in automaton['transitions']:
            # Checking if the transition's 'from' state matches the current state AND if the transition's input matches the current letter
            if transition['from'] == current_state and transition['input'] == letter:
                # If the conditions are met we update the next state to the 'to' state of the current transition
                next_state = transition['to']
                # We exit the loop
                break
        # If no transition is found for the current letter then the word doesn't exist in the automaton
        if next_state is None:
            return False
        current_state = next_state
    # If the last state is a final state then the word is recognized
    return current_state in automaton['finalStates']
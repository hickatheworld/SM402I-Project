
def recognize_word(word: str, automaton: dict):
    """
    Tests if a word is in the automaton.
    Args:
        word: the requested word which we want to compare to the automaton's language
        automaton: the automaton we want to compare the language of to the given word
    Returns:
        nothing
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
            print(f"Word {word} is not recognized by the automaton.")
            return
        current_state = next_state
    # If the last state is a final state then the word is recognized, else not
    if current_state in automaton['finalStates']:
        print(f"Word {word} is recognized by the automaton.")
    else:
        print(f"Word {word} is not recognized by the automaton.")

def is_word_recognise(automaton: dict):
    """
    Loop to test if multiples words are in the automaton
    Args:
        automaton: the automaton to analyse
    Returns:
        nothing
    """
    word = input("Enter a word to recognise, type / to stop the algorithm: ")
    # Continue looping until the user types '/'
    while word != "/":
        # Call the function to recognize the entered word to compare to the automaton
        recognize_word(word, automaton)
        word = input("Enter a word to recognise: ")

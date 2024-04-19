
def recognize_word(word, automaton): #test if a word is in the automaton
    current_state = automaton['initialStates'][0]
    for letter in word:
        next_state = None
        for transition in automaton['transitions']:
            if transition['from'] == current_state and transition['input'] == letter:
                next_state = transition['to']
                break
        if next_state is None: # if no transition is found for the current letter then the word doesn't exist in the automaton
            print(f"Word {word} is not recognized by the automaton.")
            return
        current_state = next_state
    if current_state in automaton['finalStates']: # if the last state is a final state then the word is recognized else not
        print(f"Word {word} is recognized by the automaton.")
    else:
        print(f"Word {word} is not recognized by the automaton.")

def is_word_recognise(automaton): # loop to test if multiples words are in the automaton
    word = input("Enter a word to recognise, type / to stop the algorithm: ")
    while word != "/":
        recognize_word(word, automaton)
        word = input("Enter a word to recognise: ")

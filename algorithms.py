def display_automaton(automaton):
    print("Automaton #{}".format(automaton['id']))
    print("{:9}".format("."))
    for letter in automaton['alphabet']:
        print(letter,end=' '*4)
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



if __name__ == "__main__":
    from automatas_splitter import read_automata_json 
    automatas = read_automata_json("automatas.json")
    for item in automatas:
        print("------------------------------------------------")
        display_automaton(item)

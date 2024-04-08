AUTOMATAS = {
    "automatas": [
        {
            "id": "1",
            "states": ["0"],
            "alphabet": ["a"],
            "transitions": [],
            "initialStates": ["0"],
            "finalStates": ["0"]
        },
        {
            "id": "2",
            "states": ["0"],
            "alphabet": ["a"],
            "transitions": [
                ["0", "a", "0"]
            ],
            "initialStates": ["0"],
            "finalStates": ["0"]
        },
        {
            "id": "3",
            "states": ["0", "1"],
            "alphabet": ["a"],
            "transitions": [
                ["0", "a", "1"]
            ],
            "initialStates": ["0"],
            "finalStates": ["1"]
        },
        {
            "id": "4",
            "states": ["0", "1"],
            "alphabet": ["a"],
            "transitions": [
                ["0", "a", "1"]
            ],
            "initialStates": ["0"],
            "finalStates": []
        },
        {
            "id": "5",
            "states": ["0", "1", "2", "3", "4"],
            "alphabet":["a", "b"],
            "transitions": [
                ["1", "a", "2"],
                ["1", "b", "0"],
                ["3", "a", "0"],
                ["3", "b", "4"],
                ["0", "a", "0"],
                ["0", "b", "0"]
                
            ],
            "initialStates": ["1", "3"],
            "finalStates": ["2", "4"]
        }
    ]
}

"""
## DRAFT ##
Displays an automaton's transition table
"""
def display_automaton(automaton):
    print(automaton['id'])
    print('',end=' '*9)
    for letter in automaton['alphabet']:
        print(letter,end=' '*4)
    print()
    for state in automaton['states']:
        s = ''
        s+='I' if state in automaton['initialStates'] else ' '
        s+='F' if state in automaton['finalStates'] else ' '
        s+=' '
        print(f'{s} {state}',end=' '*4)
        for l in automaton['alphabet']:
            x = ''
            for t in automaton['transitions']:
                if t[0]==state and t[1]==l:
                    x+=t[2] + ','
            x = x[:-1]
            if x=='':
                x = '-'
            print(x,end=' '*4)
        print()
display_automaton(AUTOMATAS['automatas'][4])

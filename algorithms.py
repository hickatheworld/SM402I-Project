import json
import os

def read_automata(filepath: str) -> list:
    """
    Parses automata data from given file.
    Args:
        filepath: Path of the file to parse.
    Returns:
        A list of parsed automata.
    """
    with open(filepath, "r") as data:
        content = json.loads(data.read())
        content = content["automatas"]
    return content


def save_automata(automata: list) -> None:
    """
    Saves given automata to file.
    Args:
        automata: automata to save
    """
    os.makedirs('automata', exist_ok=True)
    for automaton in automata:
        file_name = f"INT1-5-{automaton['id']}.txt"
        path = os.path.join('automata',file_name)
        with open(path, "w") as f:
            content = json.dumps(automaton, indent=4, separators=(",", ":"))
            f.write(content)


def display_automaton(automaton: dict) -> None:
    """
    WIP. Displays given automaton

    Args:
        automaton: Automaton to display
    """

    print(f"Automaton #{automaton['id']}")

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
from typing import List
import sys

def welcome_print() -> None:
    """
    Prints the program's welcome message.
    """
    print('╔═══════════════════════════════════════════════╗')
    print('║                                               ║')
    print('║                    L2 INT-1                   ║')
    print('║                     SM402I                    ║')
    print('║     Finite Automata & Regular Expressions     ║')
    print('║               Team 5\'s project                ║')
    print('║                                               ║')
    print('╚═══════════════════════════════════════════════╝')

def menu(options: List[str]) -> int:
    """
    Displays a menu and handles user input.
    Args:
        options: List of displayed menu choices.
    Returns:
        The 0-based user selection index.
    """
    # User input is 1-based, but the returned value is 0-based, 
    # To facilitate any related list operations.
    print(f'Please select an option [1-{len(options)}]:')
    for i in range(len(options)):
        print(f'{i+1}. {options[i]}')
    print()
    user_input = None
    while user_input not in range(1, len(options) + 1):
        try:
            user_input = int(input('> '))
            
        except KeyboardInterrupt:
            # The user used Ctrl-C to exit the program
            sys.exit()
        except ValueError:
            user_input = -1
            
    return user_input - 1

def choose_automaton(automata: dict) -> dict:
    """
    Lets the user choose an automaton, making sure the choice is valid.
    Args:
        automata: The list of automata to choose from.
    Returns:
        The selected automaton.
    """
    selected = None
    ids = [automaton['id'] for automaton in automata]
    print('Please select an automaton:')
    while selected not in ids:
        try:
            selected = input('> ')
        except KeyboardInterrupt:
            # The user used Ctrl-C to exit the program
            sys.exit()
        except ValueError:
            selected = None
    return automata[ids.index(selected)]

def closed_question(question: str) -> bool:
    """
    Asks a yes/np question and returns the user's answer.
    Args:
        question: The question to ask.
    Returns:
        The user's answer.
    """
    answer = ' '
    while answer not in 'yn':
        try:
            answer = input(f'{question} (Y/N) ').lower()[0]
        except KeyboardInterrupt:
            # The user used Ctrl-C to exit the program
            sys.exit()
    return answer == 'y'

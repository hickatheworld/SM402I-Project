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
    # to facilitate any related list operations.
    print(f'Please selection an option [1-{len(options)}]:')
    for i in range(len(options)):
        print(f'{i+1}. {options[i]}')
    print()
    user_input = None
    while user_input not in range(1, len(options) + 1):
        try:
            user_input = int(input('> '))
            
        except KeyboardInterrupt:
            print("Ctrl C detected : Goodbye !\n")
            # The user typed Ctrl C => Exit the program
            sys.exit()
        except ValueError:
            user_input = -1
            
    return user_input - 1

from lib import *
import Int1_5_algorithms as algo
import Int1_5_lib as libr

if __name__ == "__main__":
    libr.welcome_print()
    actions = ['Display automata', 'Exit']
    selected_action = None
    while selected_action != 1: # to replace with the index of 'exit' action when actions are changed
        selected_action = libr.menu(actions)
        match selected_action:
            case 0:
                print('todo')
        print()
    print('Good bye.')

    
        
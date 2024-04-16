from lib import *

if __name__ == "__main__":
    welcome_print()
    actions = ['Display automata', 'Exit']
    selected_action = None
    while selected_action != 1: # to replace with the index of 'exit' action when actions are changed
        selected_action = menu(actions)
        match selected_action:
            case 0:
                print('todo')
        print()
    print('Good bye.')

    
        
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
                ID = input("Give an integer ID between 1 and 44: ")
                while not('1' <= ID <= '44'):
                    ID = input("Give an integer ID between 1 and 44: ")
                automata_dict = algo.get_automaton_by_id(int(ID), "automatas.json")
                print(automata_dict)
                print('todo')
        print()
    print('Good bye.')

    
        
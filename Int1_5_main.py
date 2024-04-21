import json
from time import sleep
from src import Int1_5_algorithms as algo
from src import Int1_5_lib as libr
from src import Int1_5_standardization as stan
from src import Int1_5_determinization as dete

if __name__ == "__main__":
    libr.welcome_print()
    selected_automaton = None
    automata = json.load(open('src/automata/automata.json'))
    actions = ['List automata', 'Display automaton', 'Standardize automaton', 'Determinize automaton', 'Exit']
    selected_action = None
    # Menu starts
    while selected_action != 4:
        print('-'*5)
        selected_action = libr.menu(actions)
        match selected_action:
            case 0:
                print("List of automata:")
                for automaton in automata:
                    print(automaton['id'], end=' ')
                print()
            case 1: # Display
                selected_automaton = libr.choose_automaton(automata)
                algo.display_automaton(selected_automaton)
            case 2: # Standardize
                selected_automaton = libr.choose_automaton(automata)
                if stan.is_standard(selected_automaton):
                    print("The automaton is already standard!")
                else:
                    standardized = stan.standardize(selected_automaton)
                    print('Standardized version:')
                    algo.display_automaton(standardized)
                    save = libr.closed_question('Would you like to save it?')
                    if save:
                        algo.save_automaton(standardized)
                        print(f'{standardized["id"]} saved.')
                        automata.append(standardized)
            case 3: # Determinize
                selected_automaton = libr.choose_automaton(automata)
                if dete.is_deterministic(selected_automaton):
                    print("The automaton is deterministic!")
                    if dete.is_complete(selected_automaton):
                        print("The automaton is already complete!")
                    else:
                        completed_automaton = dete.completion(selected_automaton)
                        print('Completed automaton:')
                        algo.display_automaton(completed_automaton)
                        save = libr.closed_question('Would you like to save it?')
                        if save:
                            algo.save_automaton(completed_automaton)
                            print(f'{completed_automaton["id"]} saved.')
                            automata.append(completed_automaton)
                else:
                    print("The automaton is not deterministic")
                    determinized_automaton = dete.determinization_and_completion_automaton(selected_automaton)
                    print('Determinized automaton:')
                    algo.display_automaton(determinized_automaton)
                    save = algo.closed_question('Would you like to save it?')
                    if save:
                        algo.save_automaton(determinized_automaton)
                        print(f'{determinized_automaton["id"]} saved.')
                        automata.append(determinized_automaton)

    print('Good bye !')

    
        
import json
from time import sleep
from src import Int1_5_algorithms as algo
from src import Int1_5_lib as libr
from src import Int1_5_standardization as stan
from src import Int1_5_determinization as dete
from src import Int1_5_recognition as recog
from src import Int1_5_minimization as mini

if __name__ == "__main__":
    libr.welcome_print()
    selected_automaton = None
    automata = json.load(open('src/automata/automata.json'))
    actions = ['List automata', 'Display automaton', 'Standardize automaton', 'Determinize and complete automaton', 'Minimize automaton',
               'Try and recognize words', 'Exit']
    selected_action = None
    # Menu starts
    while selected_action != len(actions) - 1:
        print('-' * 5)
        selected_action = libr.menu(actions)
        match selected_action:
            case 0:
                print("List of automata:")
                for automaton in automata:
                    print(automaton['id'], end=' ')
                print()
            case 1:  # Display
                selected_automaton = libr.choose_automaton(automata)
                algo.display_automaton(selected_automaton)
            case 2:  # Standardize
                selected_automaton = libr.choose_automaton(automata)
                is_standard = stan.is_standard(selected_automaton)
                if is_standard == 'standard':
                    print("The automaton is already standard!")
                else:
                    print('The automaton is not standard because', 
                          'it has multiple initial states' 
                          if is_standard == 'multiple_initial_states' 
                          else 'it has a transition to the entry state')
                    standardized = stan.standardize(selected_automaton)
                    print('Standardized version:')
                    algo.display_automaton(standardized)
                    save = libr.closed_question('Would you like to save it?')
                    if save:
                        algo.save_automaton(standardized)
                        print(f'{standardized["id"]} saved.')
                        automata.append(standardized)
            case 3:  # Determinize
                selected_automaton = libr.choose_automaton(automata)
                is_deter = dete.is_deterministic(selected_automaton)
                if is_deter == 'deterministic':
                    print("The automaton is deterministic!")
                    if dete.is_complete(selected_automaton):
                        print("The automaton is already complete!")
                    else:
                        print('There is not a transition for all letters of the alphabet in each state, hence the automaton is not complete.')
                        completed_automaton = dete.completion(selected_automaton)
                        print('Completed automaton:')
                        algo.display_automaton(completed_automaton)
                        save = libr.closed_question('Would you like to save it?')
                        if save:
                            algo.save_automaton(completed_automaton)
                            print(f'{completed_automaton["id"]} saved.')
                            automata.append(completed_automaton)
                else:
                    print('The automaton is not deterministic because',end=' ')
                    match is_deter:
                        case 'async':
                            print('it has epsilon transitions.')
                        case 'multiple_initial_states':
                            print('it has multiple initial states.')
                        case 'multiple_same_label_transitions':
                            print('it has multiple transitions with the same label from the same state.')
                    determinized_automaton = dete.determinization_and_completion_automaton(selected_automaton)
                    print('Determinized automaton:')
                    algo.display_automaton(determinized_automaton)

                    save = libr.closed_question('Would you like to save it?')
                    if save:
                        algo.save_automaton(determinized_automaton)
                        print(f'{determinized_automaton["id"]} saved.')
                        automata.append(determinized_automaton)

            case 4: # Minimize
                selected_automaton = libr.choose_automaton(automata)
                result = None
                print("We need to minimize this : ")
                algo.display_automaton(selected_automaton)
                if dete.is_complete(selected_automaton) and dete.is_deterministic(selected_automaton):
                    result = mini.minimization(selected_automaton)
                    mini.display_minimal_automaton(*result)
                    save = libr.closed_question('Would you like to save it?')
                    if save:
                        algo.save_automaton(result[2])
                        print(f'{result[2]["id"]} saved.')
                        automata.append(result[2])
                else:
                    print("Operation is impossible, we must determinize and complete first.")
                    cdfa = dete.determinization_and_completion_automaton(selected_automaton)
                    print("The cdfa is this :")
                    algo.display_automaton(cdfa)
                    result = mini.minimization(cdfa)
                    mini.display_minimal_automaton(*result)
                    if result[0]: # If the automaton was not already minimal
                        save = libr.closed_question('Would you like to save it?')
                        if save:
                            algo.save_automaton(result[1])
                            print(f'{result[1]["id"]} saved.')
                            automata.append(result[1])

            case 5:  # Recognize
                selected_automaton = libr.choose_automaton(automata)
                word = input('Enter a word, or / to stop word recognition: ')
                while word != '/':
                    is_recogizned = recog.recognize_word(word, selected_automaton)
                    print(f'The word {word} is recognized by automaton #{selected_automaton["id"]}'
                          if is_recogizned else f'The word {word} is not recognized by automaton #{selected_automaton["id"]}')
                    word = input('Enter a word, or / to stop word recognition: ')
    print('Good bye !')


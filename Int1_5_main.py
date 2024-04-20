from src import Int1_5_algorithms as algo
from src import Int1_5_lib as libr
from src import Int1_5_standardization as stan
from src import Int1_5_determinization as dete

if __name__ == "__main__":
    libr.welcome_print()
    actions = ['Display automata', 'Standardize automata', 'Determinize automata', 'Exit']
    selected_action = None

    # Asking the user the ID of the automaton he wants
    print("To begin with, you will chose an automaton to work on !")
    ID = input("Give an integer ID between 1 and 44: ")
    while len(ID)> 2 or (not ('1' <= ID <= '44') and not ('5' <= ID <= '9')):
        ID = input("Give an integer ID between 1 and 44: ")
    # Creating a dictionary for the chosen automaton
    automata_dict = algo.get_automaton_by_id(int(ID), "src/automata/automatas.json")
    # Saving it into a text file
    algo.save_automaton(automata_dict)

    # Menu starts
    while selected_action != 3:
        selected_action = libr.menu(actions)
        match selected_action:
            case 0: # Display of the automaton which's ID was given
                algo.display_automaton(automata_dict)

            case 1: # STANDARDIZATION
                if stan.is_standard(automata_dict): # Checking if the automaton is standard
                    print("The automaton is standard !")
                else:
                    print("The automaton is not standard...")
                    standardize = input("Would you like to make it standard ? (Y - N) ")
                    while standardize != "Y" and standardize != "N":
                        standardize = input("Would you like to make it standard ? (Y - N) ")
                    if standardize == "Y":
                        stan.standardize(automata_dict)
                        print("Done standardizing ! \n")

            case 2: # DETERMINIZATION
                # Checking if the automataton is deterministic
                if dete.is_deterministic(automata_dict):
                    print("The automaton is deterministic !")
                    # Checking if the automaton is complete
                    if dete.is_complete(automata_dict):
                        print("The automaton is complete !")
                    else:
                        print("The automaton is not complete...")
                        print("Let's complete it...")
                        # Completing it because it's not already
                        completed_automaton = dete.completion(automata_dict)
                        print("Done completing ! \n")
                else:
                    print("The automaton is not deterministic...")
                    print("Let's complete and determinize it...")
                    determinized_automata = dete.determinization_and_completion_automaton(automata_dict)
                    print("We are now dealing with a complete deterministic finite automaton !")
                # display_complete_dererministic_automaton(CDFA)





    print('Good bye !')

    
        
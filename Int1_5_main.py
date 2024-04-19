import Int1_5_algorithms as algo
import Int1_5_lib as libr
import Int1_5_standardization as stan
import Int1_5_determinization as dete

if __name__ == "__main__":
    libr.welcome_print()
    actions = ['Display automata', 'Standardize automata', 'Determinize automata', 'Exit']
    selected_action = None

    # asking the user the ID of the automaton he wants, creating a dictionary for it, and saving it into a text file
    print("To begin with, you will chose an automaton to work on !")
    ID = input("Give an integer ID between 1 and 44: ")
    while not ((len(ID) <= 2 and ('1' <= ID <= '44')) or (len(ID) == 1 and ('5' <= ID <= '9'))):
        ID = input("Give an integer ID between 1 and 44: ")
    automata_dict = algo.get_automaton_by_id(int(ID),
                                             "automatas.json")  # creating a dictionary for the chosen automaton
    algo.save_automaton(automata_dict)  # saving it into a text file

    # Menu starts
    while selected_action != 3:
        selected_action = libr.menu(actions)
        match selected_action:
            case 0:  # displaying the automaton which's ID was given
                print(automata_dict)
                algo.display_automaton(automata_dict)

            case 1:  # stuff linked with standardization
                if stan.is_standard(automata_dict):  # checking if standard
                    print("The automaton is standard !")
                else:
                    print("The automaton is not standard...")
                    standardize = input("Would you like to make it standard ? (Y - N) ")
                    while standardize != "Y" and standardize != "N":
                        standardize = input("Would you like to make it standard ? (Y - N) ")
                    if standardize == "Y":
                        stan.standardize(automata_dict)

            case 2:  # stuff linked with determinization
                if dete.is_deterministic(automata_dict):  # checking if deterministic
                    print("The automaton is deterministic !")
                else:
                    print("The automaton is not deterministic...")

                if dete.is_complete(automata_dict):  # checking if complete
                    print("The automaton is complete !")
                else:
                    print("The automaton is not complete...")
                    print("Let's complete it !")
                    dete.completion(automata_dict)

    print('Good bye !')

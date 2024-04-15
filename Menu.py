import sys

class Menu:
    def __init__(self):
        self.choices = ["0"]     # by default, the menu only contains the option to quit it
        self.userChoice = ""
        print("\n\n|    Welcome to team 5's FA&RegEx project user interface    |")

    def quit(self):
        print("Are you sure you want to quit ? [Y/N]")
        self.userChoice = self.getUserChoice()
        if self.userChoice.lower() == "y":
            print("Bye !")
            sys.exit()
            

    def start(self):
        while self.userChoice.strip().lower() not in self.choices:
            print("> Enter a number to perform the action associated to it")
            
            # Write the possible actions for the user here

            print("\t0. Exit this program")


            self.userChoice = self.getUserChoice()
            self.manageUserChoice()
            
    def manageUserChoice(self):
        if self.userChoice == "0":
            self.quit()



    def getUserChoice(self):
        userChoice = input("\nWhat do you want to do ?\n~ ")
        return userChoice
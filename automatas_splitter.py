import json # to read and write files
import os   # to create directories if necessary 

def read_automata_json(filepath : str) -> list:
    """reads the json file, returns a list of the found automata """
    try:
        print("Reading at '{fp}' ...".format(fp=filepath))  # loading content
        with open(filepath, "r") as data:
            content = json.loads(data.read())
            content = content["automatas"]
        print("done !", len(content), "automata found in the file.")
        return content
    except:
        print("an Error occured.")
        print("note : filepath is '{fp}'".format(fp=filepath))
        return []


def write_automata_to_file(automata:list):
    """takes a list of automata and writes them to txt files"""
    team_number = "5"     # change accordingly to the team (https://discord.com/channels/1159470459709046784/1206604961564328015/1227378624194154567)
    os.makedirs("src/automata", exist_ok=True)  # create the subdirectories
    os.chdir("src/automata")    # go inside the folder
    for automaton in automata:

        file_name = "INT1-{}-{}.txt".format(team_number, automaton["id"])  # Creating directory 
        

        print("Writing ...")    # writing files in the directory
        with open(file_name, "w") as to_write:
            content = json.dumps(automaton, indent=4, separators=(",", ":"))
            to_write.write(content)
        print("Done ! wrote {} characters to {}".format(len(content), file_name))






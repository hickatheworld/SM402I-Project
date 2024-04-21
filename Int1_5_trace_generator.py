import subprocess
import json

# Fetching test automata ids to generate a trace for each one of them
f = open('src/automata/automata.json', 'r')
automata = json.load(f)
f.close()
ids = [a['id'] for a in automata]

for id in ids:
	print(f'Generating trace for automaton #{id}')
	with open(f'traces/Int1_5_{id}.txt', 'w') as f:
		# This are the inputs the user would type in the terminal
		sub_stdin = "2\n"\
		+ f"{id}\n" \
		+ "3\n" \
		+ f"{id}\n"\
		+ "n\n"\
		+ "4\n"\
		+ f"{id}\n"\
		+ "n\n"\
		+ "5\n"\
		+ f"{id}\n"\
		+ 'n\n'\
		+ '6\n'\
		+ f"{id}\n"\
		+ 'a\n'\
		+ 'aab\n'\
		+ '\n'\
		+ '/\n'\
		+ '6\n'
		# To generate the trace automatically, we simply run the program in a child process, 
  		# redirecting stdout (standard output, that is everything which would get displayed on the screen) to our trace file
		proc = subprocess.Popen(['python', 'Int1_5_main.py'], stdin=subprocess.PIPE, stdout=f, text=True)
		proc.communicate(input=sub_stdin) # Then, the inputs are sent to the program as if they were typed by the user
		proc.kill()

print(f'All {len(ids)} traces have successfully been generated.')
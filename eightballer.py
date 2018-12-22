import random
possible = [ 
"Ne",
"Ano",
"Nemyslím si",
"Zkus to znova později",
"Spíše ano",
"Raději ti to neřeknu",
"Můžeš se na to spolehnout"]
def eightball_pick():
	return random.choice(possible)
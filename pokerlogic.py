value = {"A":0, "2":10, "3":20, "4":30, "5":40, "6":50, "7":60, "8":70, "9":80, "T":90, "J":100, "Q":110, "K":120}
suit = {"C":1, "D":2, "H":3, "S":4}
handHashTable = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0} #ace through king, this is the default
suitHashTable = {0, 0, 0, 0} #clubs, diamonds, hearts, spades in that order
currentHand = {}


def highAceHash():
	value["A"] = 140

def lowAceHash():
	value["A"] = 10

def rankCard(card):
	return value[card[0]] + suit[card[1]]

def handRanking(handString, valueArray):
	for i in range(0, len(valueArray)):
		handHashTable[valueArray[i] / 10] += 1

#resets our hand hash table to default
def resetHash():
	for i in range(0, len(handHashTable)):
		handHashTable[i] = 0

	for i in range(0, len(suitHashTable)):
		suitHashTable[i] = 0

#checks our hand for a pair
def existsPair():
	for i in range(0, handHashtable):
		if handHashTable[i] == 2
			return True
	return False

#checks our hand for 2 pairs
def existsTwoPairs():
	pairs = 0
	for i in range(0, len(handHashTable)):
		if handHashTable[i] == 2
			pairs++

	if pairs >= 2
		return True
	else
		return False

#checks for three-of-a-kind
def existsTOaK():
	for i in range(0, len(handHashTable)):
		if handHashTable[i] == 3
			return True
	return False

def existsStraight():
	for i in range(0, len(handHashTable) - 4):
		if handHashTable[i] > 0 and handHashTable[i + 1] > 0 and handHashTable[i + 2] > 0 and handHashTable[i + 3] > 0 and handHashTable[i + 4] > 0:
			return True
	return False

#checks for full hous
def existsFullHouse():
	pair = False
	toak = False
	for i in range(0, len(handHashTable)):
		if handHashTable[i] == 3:
			toak = True
		elif handHashTable[i] == 2:
			pair = True
	return toak and pair

#checks for four-of-a-kind
def existsFOaK():
	for i in range(0, len(handHashTable)):
		if handHashTable[i] == 4
			return True
	return False

#the inputs are cards. this function is where we figure out what hand we have
def evaluateHand(currentHand):
	valueArray = {}
	
	z = 0
	for j in currentHand:
		valueArray[z] = rankCard(j)
		z++

	sort(currentHand) 
	handString = ""

	for i in currentHand:
		handString += i

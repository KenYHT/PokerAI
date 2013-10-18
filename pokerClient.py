import urllib, urllib2, json, random
from time import sleep

key = "6c19c9ff-9505-4084-bfae-9da533877cc2"

def getRequest(url):
  readurl = urllib2.urlopen(url).read()
  contents = json.loads(str(readurl))
  # contents = json.loads(readurl)
  return contents

#data is a set
def postRequest(url, data):
  try:
    stuff = urllib.urlencode(data)
    req = urllib2.Request(url, stuff)
    response = urllib2.urlopen(req).read()
  except:
    print "POST Request failed :("
  return response

def isCindaHere(players):
  for p in players:
    if p["player_name"] == "Cinda":
      return true

  return false

value = {"A":0, "2":10, "3":20, "4":30, "5":40, "6":50, "7":60, "8":70, "9":80, "T":90, "J":100, "Q":110, "K":120}
suit = {"C":1, "D":2, "H":3, "S":4}
handHashTable = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #ace through king, this is the default
suitHashTable = {"C":0, "D":0, "H":0, "S":0} #clubs, diamonds, hearts, spades in that order
currentHand = []
finalValue = 0


def highAceHash():
        value["A"] = 140

def lowAceHash():
        value["A"] = 10

def rankCard(card):
        return value[card[0]] + suit[card[1]]

def initHash(valueArray):
        for i in range(0, len(valueArray)):
                handHashTable[valueArray[i] / 10] += 1

        for i in range(0, len(currentHand)):
                suitHashTable[(currentHand[i])[1]] += 1

#resets our hand hash table to default
def reset():
        for i in range(0, len(handHashTable)):
                handHashTable[i] = 0

        for i in suitHashTable:
                suitHashTable[i] = 0

        for i in range(0, len(currentHand)):
                currentHand.pop()

        finalValue = 0

#checks our hand for a pair
def existsPair():
        for i in range(0, len(handHashTable)):
                if handHashTable[i] == 2:
                        return True
        return False

#checks our hand for 2 pairs
def existsTwoPairs():
        pairs = 0
        for i in range(0, len(handHashTable)):
                if handHashTable[i] == 2:
                        pairs+= 1

        if pairs >= 2:
                return True
        else:
                return False

#checks for three-of-a-kind
def existsTOaK():
        for i in range(0, len(handHashTable)):
                if handHashTable[i] == 3:
                        return True
        return False

#checks for straight
def existsStraight():
        for i in range(0, len(handHashTable) - 4):
                if handHashTable[i] > 0 and handHashTable[i + 1] > 0 and handHashTable[i + 2] > 0 and handHashTable[i + 3] > 0 and handHashTable[i + 4] > 0:
                        return True
        return False

#checks for flush
def existsFlush():
        for i in suitHashTable:
                if suitHashTable[i] >= 5:
                        return True
        return False

#checks for full house
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
                if handHashTable[i] == 4:
                        return True
        return False

#the inputs are cards. this function is where we figure out what hand we have
def evaluateHand(currentHand):
        valueArray = []
        for j in currentHand:
                valueArray.append(rankCard(j))

        print "start"
        initHash(valueArray)
        print "initialized hash"


        print "1: ", existsFOaK()
        print "2: ", existsFullHouse()
        print "3: ", existsFlush()
        print "4: ", existsStraight()
        print "5: ", existsTOaK()
        print "6: ", existsTwoPairs()
        print "7: ", existsPair()
        if existsFOaK() == True:
                finalValue = 7
        elif existsFullHouse() == True:
                finalValue = 6
        elif existsFlush() == True:
                finalValue = 5
        elif existsStraight() == True:
                finalValue = 4
        elif existsTOaK() == True:
                finalValue = 3
        elif existsTwoPairs() == True:
                finalValue = 2
        elif existsPair() == True:
                finalValue = 1
        else:
                finalValue = 0

        print "okay"


move = {"action_name": "bet", "amount": 20}
betRaise = {"action_name": "call"}
mode = "normal"

while True:
  sleep(1)  
  try:
    deal = getRequest("http://nolimitcodeem.com/api/players/"+key)
    reset()

    if not deal['your_turn']:
      print "Not my turn..."
      lost = deal['lost_at']
      if lost != None:
        print "...maaaan, I lost at ", lost
      continue

    print "My turn!!  Finally! ",
    cards = deal['hand']
    print "got cards"
    evaluateHand(cards)
    print "evaluated them"
    community_cards = deal['community_cards']
    playerNum = deal['total_players_remaining']
    money = int(deal['stack'])
    roundNum = deal['round_id']
    callAmt = deal['call_amount']
    print "> Round ", roundNum

    phase = deal['betting_phase']
    print "| "+phase+" |"

    #fold or call
    r = random.random()

    if phase == "deal":
      if callAmt >= 0.3 * money:
        move = {"action_name": "fold"}
      elif callAmt > 0:
        move = {"action_name": "call"}
    else:
      if finalValue >= 6:
        move = {"action_name": "bet", "amount": int(0.50*money)}
      elif finalValue >= 2:
          move = {"action_name": "call"}
      elif finalValue == 1 and callAmt <= 0.3*money:
        if r > 0.5:
          move = {"action_name": "call"}
        else:
          move = {"action_name": "fold"}
      else:
        if r > 0.5:
          move = {"action_name": "call"}
        else:
          move = {"action_name": "fold"}


    if random.random() > 0.99:
      move = {"action_name": "bet", "amount": int(0.90*money)}

    print "Moving ", move
    act = postRequest("http://nolimitcodeem.com/api/players/"+key+"/action", move)
    # act = postRequest("http://nolimitcodeem.com/sandbox/players/flop-phase-key/action", move)
    print act, "\n\n"

    


    #Update the mode
    if mode == "normal":
      print "> Normal action"
    elif mode == "bet high":
      print "> Betting high"
    elif mode == "all in":
      print "> All IN."

  except:
    print ">> ERROR: Something went wrong, turn was interrupted somehow :("
  # print deal["your_turn"]
  # deal["hand"]
  # deal["community_cards"]
  # deal["betting_phase"]
  # players = deal["players_at_table"]
  # isCindaHere(players)


  # print deal







  # deal = "{\"name\":\"Bill16\",\"your_turn\":true,\"initial_stack\":250,\"stack\":250,\"current_bet\":null,\"call_amount\":10,\"hand\":[\"9S\",\"KS\"],\"betting_phase\":\"deal\",\"players_at_table\":[{\"player_name\":\"Bill16\",\"initial_stack\":250,\"current_bet\":0,\"stack\":250,\"folded\":false,\"actions\":[]},{\"player_name\":\"Bill17\",\"initial_stack\":250,\"current_bet\":5,\"stack\":245,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":5}]},{\"player_name\":\"Bill18\",\"initial_stack\":250,\"current_bet\":10,\"stack\":240,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":10}]}],\"total_players_remaining\":3,\"table_id\":427,\"round_id\":447,\"round_history\":[{\"round_id\":447,\"table_id\":427,\"stack_change\":null}],\"lost_at\":null,\"community_cards\":[]}"
  # flop = "{\"name\":\"Bill16\",\"your_turn\":true,\"initial_stack\":250,\"stack\":160,\"current_bet\":90,\"call_amount\":0,\"hand\":[\"Ac\",\"As\"],\"betting_phase\":\"flop\",\"players_at_table\":[{\"player_name\":\"Bill16\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"bet\",\"amount\":80}]},{\"player_name\":\"Bill17\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":5},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0}]},{\"player_name\":\"Bill18\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":10},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0}]}],\"total_players_remaining\":3,\"table_id\":427,\"round_id\":447,\"round_history\":[{\"round_id\":447,\"table_id\":427,\"stack_change\":null}],\"lost_at\":null,\"community_cards\":[\"3c\",\"3d\",\"4c\"]}"
  # turn = "{\"name\":\"Bill16\",\"your_turn\":true,\"initial_stack\":250,\"stack\":160,\"current_bet\":90,\"call_amount\":0,\"hand\":[\"Ac\",\"As\"],\"betting_phase\":\"turn\",\"players_at_table\":[{\"player_name\":\"Bill16\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"bet\",\"amount\":80},{\"action\":\"bet\",\"amount\":0}]},{\"player_name\":\"Bill17\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":5},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0}]},{\"player_name\":\"Bill18\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":10},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0}]}],\"total_players_remaining\":3,\"table_id\":427,\"round_id\":447,\"round_history\":[{\"round_id\":447,\"table_id\":427,\"stack_change\":null}],\"lost_at\":null,\"community_cards\":[\"3c\",\"3d\",\"4c\",\"4h\"]}"
  # river = "{\"name\":\"Bill16\",\"your_turn\":true,\"initial_stack\":250,\"stack\":160,\"current_bet\":90,\"call_amount\":0,\"hand\":[\"Ac\",\"As\"],\"betting_phase\":\"river\",\"players_at_table\":[{\"player_name\":\"Bill16\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"bet\",\"amount\":80},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0}]},{\"player_name\":\"Bill17\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":5},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0}]},{\"player_name\":\"Bill18\",\"initial_stack\":250,\"current_bet\":90,\"stack\":160,\"folded\":false,\"actions\":[{\"action\":\"ante\",\"amount\":10},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0},{\"action\":\"bet\",\"amount\":0}]}],\"total_players_remaining\":3,\"table_id\":427,\"round_id\":447,\"round_history\":[{\"round_id\":447,\"table_id\":427,\"stack_change\":null}],\"lost_at\":null,\"community_cards\":[\"3c\",\"3d\",\"4c\",\"4h\",\"5d\"]}"



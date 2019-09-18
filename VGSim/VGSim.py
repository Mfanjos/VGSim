import math 
import copy
import random
import string
import sys
import time

class Card:
    def __init__(self, name, grade, type, power, shield, critical, ability):
        self.name = name
        self.grade = grade
        self.type = type    #Tipos: Normal, Critical, Draw, Heal, Front.
        self.power = power
        self.shield = shield
        self.critical = critical
        self.ability = ability #Boost, Intercept


class Deck:
    def __init__(self, name, cards, gift):
        self.name = name
        self.cards = cards
        self.gift = gift

    def addcard(self, card):
        self.cards.append(card)

    def popcard(self):
        return self.cards.pop()

    def averageshield(self):
        for x in self.cards:
            shieldvalue += x.shield 
        averageshield = shieldvalue/ self.cards.len()
        return shieldvalue
   
    
def readDecksFile(filename, DeckName, Gift):
    NewDeck = Deck(DeckName, [], Gift)
    with open("DeckMuras.txt","r") as f:
        for line in f:
             words = line.split()
             ThisCard = Card(words[0], words[1], words[2], words[3], words[4], words[5], words[6])
             NewDeck.addcard(ThisCard)
    return NewDeck


def checkExistence(list, target):
    counter = 0
    for X in list:
        if X.name == target:
            counter += 1
    return counter


def getInfo():
    SimNumberW = input("How many simulations would you like to run?  ")
    try:
        SimNumber = int(SimNumberW)
    except ValueError:
        print("This is not a valid number.")
        sys.exit(0)

    filename = input("What's the filename of your deck?  ")
    DeckName = input("What's your deck's name?  ")
    Gift = input("Which Gift do you use? If you use AccelII please write it like shown.  ")
    turns = input("Fow how many turns do you want to run each simulation? (both players' turn count towards the number)  ")
    MulliganW = input("How many cards will you mulligan each game, 0-5?  ")
    try:
        Mulligan = int(MulliganW)
    except ValueError:
        print("This is not a valid number.")
        sys.exit(0)
    if Mulligan not in range(1,5):
        print("This is not a valid number.")
        sys.exit(0)
    TargetCard = input("Tell us which card you would like to target.  ")
    ListInfo = [SimNumber, filename, DeckName, Gift, turns, Mulligan, TargetCard]
    return ListInfo


def DriveCheck(n, Hand, Deck):
    DrawT = 0
    for X in range(n):
        Hand.append(Deck.popcard())
        if Hand[-1].type == "Draw":    
            Hand.append(Deck.popcard())
            DrawT += 1
    return DrawT


def DamageCheck(n, Damage, Hand, Deck):
    DrawT = 0
    for X in range(n):
        Damage.append(Deck.popcard())
        if Damage[-1].type == "Draw":    
            Hand.append(Deck.popcard())
            DrawT += 1
    return DrawT


def Sim():
    ListInfo = getInfo()
    SimNumber = ListInfo[0]
    filename = ListInfo[1]
    DeckName = ListInfo[2]
    Gift = ListInfo[3]
    turns = ListInfo[4]
    Mulligan = ListInfo[5]
    TargetCard = ListInfo[6]
       
    print("SimNumber- " + str(SimNumber))
    print("Filename- " + filename)
    print("DeckName- " + DeckName)
    print("Gift- " + Gift)
    print("Turns- " + str(turns))
    print("Mulligan- " + str(Mulligan))
    print("TargetCard- " + TargetCard)

    #Gets Deck
    SimDeckReset = readDecksFile(filename, DeckName, Gift)
    SimDeck = copy.deepcopy(SimDeckReset)
    SimDeck.gift = SimDeckReset.gift = Gift
    Successes = 0
    ToDamage = 0
    i = 0
    DrawTotal = 0

    #Starts Sim
    start_time = time.time()
    while i <= int(SimNumber):

        SimDeck = copy.deepcopy(SimDeckReset)
        SimDeck.gift = SimDeckReset.gift
        random.shuffle(SimDeck.cards)
        DrawnCards = []
        Damage = []
        DrawT = 0
        WentFirst = TurnPlayer = random.randint(0,1)

        #Game Start and Mulligan + first draw and starter
        for Y in range(7 + Mulligan):
            DrawnCards.append(SimDeck.popcard())

        #Turn Loop
        for X in range(int(turns)):
            #Until turn 4 both players drive check 1 card, if we went second our 4th turn we drive 1
            if (X < 4 and TurnPlayer == 1) or (X == 4 and TurnPlayer == 1 and WentFirst == 0):
                #Draw
                DrawnCards.append(SimDeck.popcard())
                #Drive Check if not the first turn
                if X != 0:
                    DrawT += DriveCheck(1, DrawnCards, SimDeck)
            
            elif X <= 4 and TurnPlayer == 0:
                if (X == 3 and WentFirst == 1) or (X == 2 and WentFirst == 0):
                    DrawT += DamageCheck(1, Damage, DrawnCards, SimDeck)

            #After and including turn 4
            elif X >= 4 and TurnPlayer == 1: 
                #Draw
                DrawnCards.append(SimDeck.popcard())
                if SimDeck.gift == "AccelII":
                    DrawnCards.append(SimDeck.popcard())
                #Check for target and Return
                if (X == 6 and WentFirst == 1) or (X == 7 and WentFirst == 0):
                    if checkExistence(DrawnCards, TargetCard) != 0:
                        Successes += 1
                    ToDamage += checkExistence(Damage, TargetCard)
                    break
                    
                #Drive Checks
                DrawT += DriveCheck(2, DrawnCards, SimDeck)

            #Damage and damage checks
            elif X >= 4 and TurnPlayer == 0:
                if (WentFirst == 1 and X == 5) or (WentFirst == 0  and X == 6):
                    DrawT += DamageCheck(2, Damage, DrawnCards, SimDeck)

                elif WentFirst == 0 and X == 4:
                    DrawT += DamageCheck(1, Damage, DrawnCards, SimDeck)


            #Next Iteration
            TurnPlayer = not TurnPlayer

        DrawTotal += DrawT
        i += 1

    FinalResult = Successes/SimNumber * 100
    DrawPerGame = DrawTotal/SimNumber
    ToDamage = ToDamage/SimNumber

    print("\nAfter "+ str(SimNumber) +" simulations, the percentage of games with target card in hand by second ride to grade 3 is " + str(FinalResult) + "%\n")
    print("On average target card appeared in damage " + str(ToDamage) + " times per game.\n") 
    print("On average there were " + str(DrawPerGame) + " draw triggers seen per game.\n")
    print("--- %s seconds ---" % (time.time() - start_time))


Sim()
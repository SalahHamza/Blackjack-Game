#!/usr/bin/env python
'''
    File name: blackjack.py
    Author: Salah Hamza
    Date created: --/05/2017
    Date last modified: 01/02/2018
    Python Version: 2.7
'''
import random, itertools

class Deck:

    def __init__(self):
        self.deck =list(itertools.product(["ACE"]+[str(x) for x in xrange(2,11)]+\
                        ["Jack","Queen","King"],["Diamonds","Clubs","Hearts","Spades"]))
        self.shuffle_Deck()

    def shuffle_Deck(self):
        random.shuffle(self.deck)

#class of black jack player, this will be a base class for a derived player class & dealer class
class BjPlayer:
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.hand_count = 0

    #when card is dealt this method gets the card for the player/dealer
    def get_Card(self,card):
        self.hand.append(card)

    #at the end of each round the player's hand and count needs to be emptied, this method deals with that
    def empty_Hand(self,other):
        other+=self.hand
        self.hand_count = 0
        self.hand = []

    #this will return the hand of the player/dealer, each card on the form of (e.i 10_Spades ) 
    def get_Hand(self):
        return ["_".join(x) for x in self.hand]

    def get_Lastcard(self):
        return self.get_Hand()[-1]

    #after each card printed this will show what the player/dealer has got
    def print_Lastcard(self):
        print "{} got: |{}|".format(self.name,self.get_Lastcard())

    #hand count getter
    def get_Count(self):
        return self.hand_count

    #i know this is not really necessary, but i've seen it get repeated several times, so i decided to make this method
    def print_Hand_Worth(self):
        print "{}'s hand: {}\nworth {}".format(self.name,self.get_Hand(),self.get_Count())


    def adjust_Count(self):
        current = self.hand[-1]
        if current[0] in str(range(2,11)):
            self.hand_count += int(current[0])
        elif current[0] in ["Jack","Queen","King"]:
            self.hand_count += 10
        else:
            if (self.hand_count+11) > 21:
                self.hand_count += 1
            else:
                self.hand_count +=11

    #this method returns True if player/dealer has a blackjack-natural, returns False, else.
    def has_BJ(self):
        card_val = [card_num[0] for card_num in self.hand]
        if "ACE" in card_val:
            if (("Jack" in card_val) or
                    ("Queen" in card_val) or
                        ("King" in card_val)):
                return True
        return False

    #this method checks if the player has busted
    def is_bust(self):
        if self.hand_count >21:
            return True
        return False


class Dealer(BjPlayer):
    def __init__(self,name="Dealer"):
        BjPlayer.__init__(self,name)

    def deal_Card(self,deck):
        return deck.pop()
    
class Player(BjPlayer):
    def __init__(self,name="Anonymous"):
        BjPlayer.__init__(self,name)
        self.bankroll = 0
        self.winnings = 0
        self.losses = 0
        BjPlayer.__init__(self,name)

    #this method adjusts the player's Bankroll
    def adjust_Bankroll(self):
        while True:
            try:
                amount = int(raw_input("How much money will you place?(Enter amount)\n"))
            except ValueError:
                print "Enter a valid number."
            else:
                break
        self.bankroll += amount

    #setting the game bet, with a minimum bet of 15$, incase player is betting chips more than he has, i'll ask if he wants to place money
    def set_Bet(self):
        while True:
            try:
                self.bet = int(raw_input("Enter betting amount:"))
                if self.bet <15 or (self.bet > self.bankroll):
                    if self.bet > self.bankroll:
                        print "you don't have that much money on you Mr.{}".format(self.name)
                        print "unless you want to ask for more chips by placing money."
                        rep = raw_input("do you want to place more money(y:Yes/else:No):")
                        if rep[0] == 'y':
                            adjust_Bankroll()
                    raise Exception("Minimum betting amount is 15$. Try again.")
            except ValueError:
                print "Enter a valid number."
            except Exception as ex:
                print(ex)
            else:
                break

    #set players winnings, if player wins by blackjack (aka: natural) ratio goes 3:2 so win_p=1.5
    #if player wins by a normal hand, win_p=1
    def set_Wins(self,win_p=1):
        self.winnings +=self.bet*win_p
        self.bankroll += self.bet

    #winnings getter
    def get_Wins(self):
        return self.winnings
    
    #loss setter
    def set_Loss(self):
        self.losses += self.bet
        self.bankroll-=self.bet

    #loss getter
    def get_Losses(self):
        return self.losses

    #this method will only the player's answer if he wants to Hit or stand, that's why i decided to make static
    #i am not sure if that's how static methods work
    #i thought i should use this also to ask if player wants to play another round
    @staticmethod
    def hit(Q="Do you want to hit?(Y:yes/else:no):"):
        while True:
            try:
                answer = raw_input(Q).lower()
                if answer[0] == "y":
                    return True
                else:
                    return False
            except IndexError:
                return False


#this is just a normal procedure (i don't know if that's how it's called)
def print_Line():
    print "---------------------------------"






#this is the blackjack procedure
def blackjack(bj_deck,player,dealer):
    player.set_Bet()
    print_Line()
    #first deal, dealing two cards, both showing face up for the player, only one face up for the dealer
    for i in xrange(2):
        card = dealer.deal_Card(bj_deck)
        player.get_Card(card)
        player.adjust_Count()
        player.print_Lastcard()
        card = dealer.deal_Card(bj_deck)
        dealer.get_Card(card)
        dealer.adjust_Count()
        if i!=1:
            dealer.print_Lastcard()
    print_Line()
    player.print_Hand_Worth()
    if player.has_BJ():
        dealer.print_Hand_Worth()
        print_Line()
        if dealer.has_BJ():
            print 'PUSH'
            return
        else:
            print 'Mr.{} wins this round'.format(player.name)
            player.set_Wins(1.5)
            return
    else:
        while True:
            if not player.hit():
                print "{} stands".format(player.name)
                break
            card = dealer.deal_Card(bj_deck)
            player.get_Card(card)
            player.adjust_Count()
            player.print_Lastcard()
            player.print_Hand_Worth()
            print_Line()
            if player.is_bust():
                player.print_Hand_Worth()
                dealer.print_Hand_Worth()
                print "{} BUSTs".format(player.name)
                player.set_Loss()
                return
        print_Line()
        player.print_Hand_Worth()
        dealer.print_Hand_Worth()
        if player.get_Count() > dealer.get_Count() > 16:
            print 'Mr.{} wins this round'.format(player.name)
            player.set_Wins()
        elif (player.get_Count() == dealer.get_Count() and dealer.get_Count()>16):
            print "push"
        elif dealer.get_Count() > player.get_Count() and (not dealer.is_bust()):
            print "The house wins this round"
            player.set_Loss()
        else:
            while dealer.get_Count() <= 16 and dealer.get_Count() <= player.get_Count():
                card = dealer.deal_Card(bj_deck)
                dealer.get_Card(card)
                dealer.adjust_Count()
                dealer.print_Lastcard()
                if dealer.is_bust():
                    dealer.print_Hand_Worth()
                    print "{} BUSTs".format(dealer.name)
                    print 'Mr.{} wins this round'.format(player.name)
                    player.set_Wins()
                    return
            print_Line()
            dealer.print_Hand_Worth()
            if dealer.get_Count() > player.get_Count():
                print "The house wins this round"
                player.set_Loss()
                return
            elif dealer.get_Count() == player.get_Count():
                print 'PUSH'
                return
            else:
                'Mr.{} wins this round'.format(player.name)
                player.set_Wins()
                return

        
def main():
    print "Welcome to Balckjack."
    print "Rules are clear. you'll be playing against an automated dealer\nMinimum betting amount is 15$, there is no betting limit"
    print "Wins are:\nif you get 'Blackjack' you will receive +150%(i.e 50$ will win you an additional 75$), other than that win as much as you bet (i.e 50 will win you an additional 50)."
    name = raw_input("Enter your name:")
    if name == "":
        name = "Anonymous"
    player = Player(name)
    print "Good evening Mr.{}".format(player.name)
    dealer = Dealer()
    bj_deck = Deck()
    player.adjust_Bankroll()
    while True:
        bj_deck.shuffle_Deck()
        blackjack(bj_deck.deck,player,dealer)
        player.empty_Hand(bj_deck.deck)
        dealer.empty_Hand(bj_deck.deck)
        print_Line()
        print "Your winnings: {}".format(player.get_Wins())
        print "your losses: {}".format(player.get_Losses())
        print "Total bankroll: {}".format(player.bankroll)
        print_Line()
        yes = player.hit("do you want to go another round?(y:Yes/else:No)\n")
        if not yes:
            print "Hope we see you again Mr.{}, Goodbye!".format(player.name)
            break


if __name__ == "__main__":
    main()

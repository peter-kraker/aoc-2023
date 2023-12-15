#!/usr/bin/python3

import sys

card_ranks = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

hand_ranks = {
            7 : "Five of a Kind",
            6 : "Four of a Kind",
            5 : "Full House",
            4 : "Three of a kind",
            3 : "Two Pair",
            2 : "One Pair",
            1 : "High Card"
        }

# The Game class contains a list of hands, sorts them, and can display the total winnings

class Game():
    def __init__(self, hands):
        self.hands = hands
        self.hands.sort()

    def totalWinnings(self):
        total = 0
        for i, hand in enumerate(self.hands):
            total += ((i+1) * hand.getBid())
        return total

# The Hand class takes a hand string (e.g. 32T3K 765), parses the hand, saves
# the bid, and determines what kind of hand it is.

class Hand():
    def __init__(self, card_line):

        hand, bid = card_line.split()

        self.hand = hand
        self.bid = int(bid)

        # Build a dict of all possible cards: e.g. {'A': 0, 'K': 0 ... '2': 0}
        self.cards = dict.fromkeys(card_ranks, 0)

        # Counts will contain how many of each card we saw. 
        #   For 32T3K: {1: '2', 'T', 'K'; 2: '3'}

        self.counts = dict.fromkeys(range(1,6))
        for i in self.counts:
            self.counts[i] = set()

        self.rank = self.setRank()

    def getBid(self):
        return self.bid

    def __repr__(self):
        return 'Hand: %s, Bid: %s' % (self.hand, self.bid)

    def __str__(self):
        return 'Hand: %s, Bid: %s' % (self.hand, self.bid)

    def __eq__(self, other):
#        print(self.hand, other.hand)
        return self.counts == other.counts

    def __lt__(self, other):
#        print('\t%s against %s' % (hand_ranks[self.getType()], hand_ranks[other.getType()]))
        if self.getType() == other.getType():
            if self.hand == other.hand:
                return False
            for i, c in enumerate(self.hand):
                my_card = card_ranks.index(c)
                their_card = card_ranks.index(other.hand[i])
#                print(my_card, their_card)
                if my_card == their_card:
                    continue
                elif my_card > their_card:
#                    print('\t%s is lt %s -- based on card order' % (self.hand, other.hand))
                    return True
                else:
#                    print('\t%s is not lt %s -- based on card order' % (self.hand, other.hand))
                    return False
        elif self.getType() > other.getType():
#            print('\t\t%s is not lt %s' % (hand_ranks[self.getType()], hand_ranks[other.getType()]))
            return False
        else:
#            print('\t\t%s is lt %s' % (hand_ranks[self.getType()], hand_ranks[other.getType()]))
            return True

# I probably didnt' need to implement the rest of these, since it seems sort() 
#   only uses __lt__

    def __lte__(self, other):
        if self.getType() == other.getType():
            for i, c in enumerate(self.hand):
                if card_ranks.index(c) >= card_ranks.index(other.hand[i]):
                    return True
                else:
                    continue
            return False
        elif self.getType() > other.getType():
            return False
        else:
            return True

    def __gt__(self, other):
        if self.getType() == other.getType():
            for i in range(1,6):
                if card_ranks.index(self.hand[i]) < card_ranks.index(other.hand[i]):
                    continue
                else:
                    return True 
 #           print('%s is not gt %s' % (self.hand, other.hand))
            return False
        elif self.getType() <= other.getType():
            return False
        else:
            return True

    def __gte__(self, other):
        if self.getType() == other.getType():
            for i in range(1,6):
                if card_ranks.index(self.hand[i]) <= card_ranks.index(other.hand[i]):
                    continue
                else:
#                    print('%s is gte %s' % (self.hand, other.hand))
                    return True 
#            print('%s is not gte %s' % (self.hand, other.hand))
            return False
        elif self.getType() < other.getType():
#            print('%s is not gte %s' % (self.getType(), other.getType()))
            return False
        else:
            return True

    def getType(self):
        return self.rank

    def setRank(self):
        for c in self.hand:
            if self.cards[c]:
                self.cards[c] += 1
            else:
                self.cards[c] = 1

        self.cards = dict(filter(lambda x: x[1] > 0, self.cards.items()))

        for card, count in self.cards.items():
            self.counts[count].update(card)

        self.counts = dict(filter(lambda x : len(x[1]) != 0, self.counts.items()))

        counts = list(map(lambda x: (x[0], len(x[1])), self.counts.items()))
        counts.sort(key=lambda x : x[0], reverse=True)

        high = counts.pop(0)
        match high[0]:
            case 5:
                return 7
            case 4:
                return  6
            case 3:
                low = counts.pop(0)
                match low[0]:
                    case 1:
                        return 4
                    case 2:
                        return 5
            case 2:
                low = counts.pop(0)
                match high[1]:
                    case 1:
                        return 2
                    case 2:
                        return 3
                match low[0]:
                    case 3:
                        return 5
            case 1:
                match high[1]:
                    case 5:
                        return 1


def main():
    io = open(sys.argv[1], 'r')
    inp = io.readlines()

    hands = []
    for line in inp:
        hands.append(Hand(line))

    game = Game(hands)

    print(game.totalWinnings())
    


if __name__ == '__main__':
    main()

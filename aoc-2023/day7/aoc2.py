#!/usr/bin/python3

import sys


#class Game():


card_ranks = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

hand_ranks = {
            7 : "Five of a Kind",
            6 : "Four of a Kind",
            5 : "Full House",
            4 : "Three of a kind",
            3 : "Two Pair",
            2 : "One Pair",
            1 : "High Card"
        }
            
class Game():
    def __init__(self, hands):
        self.hands = hands
        self.hands.sort()

    def totalWinnings(self):
        total = 0
        for i, hand in enumerate(self.hands):
            total += ((i+1) * hand.getBid())
        return total



class Hand():
    def __init__(self, card_line):

        hand, bid = card_line.split()
        self.hand = hand
        self.bid = int(bid)
        self.cards = dict.fromkeys(card_ranks, 0)

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
        print(self, other)
        print('\t%s against %s' % (hand_ranks[self.getType()], hand_ranks[other.getType()]))
        if self.getType() == other.getType():
            if self.hand == other.hand:
                return False
            for i, c in enumerate(self.hand):
                my_card = card_ranks.index(c)
                their_card = card_ranks.index(other.hand[i])
                print(my_card, their_card)
                if my_card == their_card:
                    continue
                elif my_card > their_card:
                    print('\t%s is lt %s -- based on card order' % (self.hand, other.hand))
                    return True
                else:
                    print('\t%s is not lt %s -- based on card order' % (self.hand, other.hand))
                    return False
        elif self.getType() > other.getType():
            print('\t\t%s is not lt %s' % (hand_ranks[self.getType()], hand_ranks[other.getType()]))
            return False
        else:
            print('\t\t%s is lt %s' % (hand_ranks[self.getType()], hand_ranks[other.getType()]))
            return True

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

        self.cards = dict(filter(lambda x : x[1] > 0, self.cards.items()))

        if 'J' in self.cards.keys():
            print(self.cards.keys())
            if list(self.cards.keys()) == ['J']:
                return 7

            num_nokers = self.cards.pop('J')[1]
            best_rank = 0
            while num_jokers:
                # TODO: Figure out how to apply Jokers to "the best" hand
                



        for card, count in self.cards.items():
            self.counts[count].update(card)

        self.counts = dict(filter(lambda x : len(x[1]) != 0, self.counts.items()))

        counts = list(map(lambda x: (x[0], len(x[1])), self.counts.items()))
        counts.sort(key=lambda x : x[0], reverse=True)

        high = counts.pop(0)
        # What happens if we just inflate everyone's hand by one type
        match high[0]:
            case 5: # Five of a kind
                return 7
            case 4: # Four of a Kind 
                return 6 
            case 3: # Either Three of Kind or Full House
                low = counts.pop(0)
                match low[0]:
                    case 1: # If there are two single cards, it's a three of a kind
                        return 4
                    case 2: # If there is a pair, it's a full house
                        return 5
            case 2: # If we have pairs, figure out how many
                match high[1]:
                    case 1: # We only have one pair
                        return 2
                    case 2: # We have two pair
                        return 3
                low = counts.pop(0)
                match low[0]:
                    case 3: # If the other set is a three of a kind, it's a full house
                        return 5
            case 1: # If we only have single cards, find out how many.
                match high[1]:
                    case 5: # If there are 5 single cards, we're high-card.
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

#!/usr/bin/python

import sys
import re

class Card():

    # I thougt I was going to parse outside the constructor... unused
    def __init__(self, card_num, winning, numbers):
        self.card_num = int(card_num)
        self.winning = winning 
        self.numbers = numbers


    # Card Constructor:
    # Takes a line of input, parses the line, and builds a 'Card' object
    # 
    # self.winning initially is the set of all winning numbers, but is winnowed
    # down via set intersection to only the numbers that match.
    #

    def __init__(self, line):
        self.winning = set()
        self.numbers = set()
        self.card_num = None
        self.count = None

        # In each line, we care about three things: 
        #   (1) the card number, 
        #   (2) The winning numbers
        #   (3) The numbers seen under the scratch-off
        # 
        # This regex pull each of those into a 'group' via the match object

        parse = re.compile(r'Card *(?P<card_num>\d*): (?P<winning>[\d ]*) \| (?P<seen>[\d ]*)$')
        line_scan = re.match(parse, line).groupdict()

        self.card_num = int(line_scan['card_num'])

        self.winning = set(line_scan['winning'].split())
        self.numbers = set(line_scan['seen'].split())

        # in-place update
        self.winning.intersection_update(self.numbers)
    

    def getCardNum(self):
        return self.card_num

    # List out which cards you get a copy of from this card.
    def getNext(self):
        return list(range(self.card_num + 1, self.card_num + len(self.winning)+1))

    # recursive method to figure out how many cards each card expands to
    def getCount(self, card_list):

        # if we've seen this card, just return it's value
        if self.count:
           return self.count

        # Otherwise, do the recursion thing.
        count = 1
        if self.getNext() is None:
            self.count = 1 # Save the value for next time
            return self.count
        for card in self.getNext():
            # Cards came in-order, so we can just use the index as the ID
            count += card_list[card-1].getCount(card_list)

        self.count = count
        return self.count 



def main():
  io = open(sys.argv[1], 'r')
  inp = io.readlines()

  # Let's go through the list, and build our deck of cards.
  card_list = []
  for line in inp:
      card_list.append(Card(line))
  
  # Now that we know which cards we have, let's count them up recursively
  total = 0
  for card in card_list:
      score = card.getCount(card_list)
      total += score

  print(total)
        

if __name__ == '__main__':
    main()

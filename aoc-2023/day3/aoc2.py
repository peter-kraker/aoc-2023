#!/usr/bin/python3

import sys
import re

# Base class to represent an item -- has an identifier, and a x / y coordinate

class Item():

    def __init__(self, iden, x, y):
        self.iden = iden
        self.x = x
        self.y = y

    def __str__(self):
        return self.iden + ": (" + str(self.x) + ", " + str(self.y) + ")"

    def isNextTo(self, x, y):
        if abs(self.x - x) <= 1 and abs(self.y - y) <= 1:
            return True
        else:
            return False

    def getIden(self):
        return self.iden

    def getX(self):
        return self.x

    def getY(self):
        return self.y


# Class to represent a 'Part.' The part has a range of x-coordinates.
#

class Part(Item):
    
    def __init__(self, part_num, start_x, end_x, y):
        self.start_x = start_x
        self.end_x = end_x - 1
        self.y = y
        self.part_num = part_num

    def __str__(self):
        return "Part " + str(self.part_num) + ": (" + str(self.start_x) + "-" + str(self.end_x) + ", " + str(self.y) + ")"

    # Part.overlaps() checks if the part's x coordinates overlaps with another
    # item.
    def overlaps(self, item: Item):
        if self.start_x <= item.getX() + 1 and item.getX() - 1 <= self.end_x:
            return True
        else:
            return False

    def isNextTo(self, item: Item):
        if self.overlaps(item) and abs(self.y - item.y) <= 1:
            return True
        else:
            return False

    def getPartNum(self):
        return self.part_num


class Gear(Item):

    def __init__(self, symbol: Item, left: Part, right: Part):
        if symbol.getIden() != "*":
            raise ValueError("This isn't a gear!")

        if left.isNextTo(symbol) and right.isNextTo(symbol):
            self.left = left
            self.right = right
            self.symbol = symbol
        elif left.isNextTo(symbol) and not right.isNextTo(symbol):
            raise ValueError("The two parts aren't adjacent to the gear! %s " % (right))
        elif not left.isNextTo(symbol) and right.isNextTo(symbol):
            raise ValueError("The two parts aren't adjacent to the gear! %s " % (left))
        else:
            raise ValueError("Neither part is adjacent to the gear! %s, %s, %s " % (symbol, left, right))

    def getRatio(self):
        return int(self.left.getPartNum()) * int(self.right.getPartNum())


def getSymbolsAndParts(inp):

    parts_re = re.compile(r'(?P<parts>\d*){,}')     # Only look for digits
    symbols_re = re.compile(r'(\*){,}')             # Only look for '*'
    
    y = 0
    part_list = []
    symbol_list = []

    for line in inp:
        line = line.rstrip()                # Remove the trailing whitespace
        parts = parts_re.finditer(line)     # scan the line and match the parts
        symbols = symbols_re.finditer(line) # ^ do the same for symbols (e.g. *)

        for part in parts:
            
            # re.finditer() returns all the non-matches too.
            # We have to check to make sure we only look at the matches.
            #
            # Add matches to the list of parts we found on this line.

            if part.group() != '':          
                part_list.append(Part(part.group(), part.start(), part.end(), y))

        for symbol in symbols:
            if symbol.group() != '':
                symbol_list.append(Item(symbol.group(), symbol.start(), y))
        y += 1

    return symbol_list, part_list


# Use all the objects we defined above to check adjacencies.

def checkAdjacencies(symbol_list, part_list):
    gears = []
    for symbol in symbol_list:

        # Because the input seems well-formatted, we can stop after we find 
        # A left and right part.
        left = None
        right = None
        
        # Optimization opportunity: sort the lists, ignore parts that have
        # no possibility of being adjacent to a symbol. 
        for part in part_list:
            if part.isNextTo(symbol):
                if left is None:
                    left = part
                elif right is None:
                    right = part
                    gears.append(Gear(symbol, left, right))
                    break
                else:
                    break
    return gears


def main():
    io = open(sys.argv[1], 'r')
    inp = io.readlines()

    symbol_list = []
    part_list = []

    # Scan the input, build a list of symbols (i.e. '*') and parts.
    symbol_list, part_list = getSymbolsAndParts(inp)

    # Now that we've scanned the input, let's check for adjacencies.
    gears = checkAdjacencies(symbol_list, part_list)

    total = 0
    for gear in gears:
        total += int(gear.getRatio())
    print(total)
    io.close()


if __name__ == '__main__':
    main()

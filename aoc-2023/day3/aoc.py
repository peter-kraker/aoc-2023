#!/usr/bin/python3

import sys
import re

# In a 2D map, find all part numbers (i.e. numeric IDs adjacent to a symbol)
# The answer is the sum of these part numbers.

# Base class to represent something in the map.
#
# Stores a part's ID (part numbe or symbol), and it's x/y coordinates.
class Item():

    def __init__(self, iden, x, y):
        self.iden = iden
        self.x = x
        self.y = y

    def __str__(self):
        return self.iden + ": (" + str(self.x) + ", " + str(self.y) + ")"

    def isNextTo(self, x, y):
        if abs(self.x - x) < 1 and abs(self.y - y) < 1:
            return True
        else:
            return False

# A Part class to represent a part number in the map.
#
# Parts are 'wide' and take up multiple x-coordinates. We need to store a range
class Part(Item):

    def __init__(self, part_num, start_x, end_x, y):
        self.start_x = start_x
        self.end_x = end_x - 1
        self.y = y
        self.part_num = part_num

    def __str__(self):
        return "Part " + str(self.part_num) + ": (" + str(self.start_x) + "-" + str(self.end_x) + ", " + str(self.y) + ")"

    # The Part.overlaps() method determines if a part's x coordinates are
    # overlapped. Ignores the y coordinates.
    def overlaps(self, item: Item):
        if self.start_x <= item.x + 1 and item.x - 1 <= self.end_x:
            return True
        else:
            return False

    # Part.isNextTo() is used to check adjacency 
    def isNextTo(self, item: Item):
        if self.overlaps(item) and abs(self.y - item.y) <= 1:
            return True
        else:
            return False

    def getPartNum(self):
        return self.part_num

def main():
    io = open(sys.argv[1], 'r')
    inp = io.readlines()

    parts_re = re.compile(r'(?P<parts>\d*){,}')
    symbols_re = re.compile(r'(?P<symbols>[^0-9.]){,}')

    y = 0
    part_list = []
    symbol_list = []

    # Iterate throug the lines, looking for Parts and Symbols.
    #
    # Store the part numbers as 'Parts' and Symbols as 'Items'
    for line in inp:
        line = line.rstrip()
        parts = parts_re.finditer(line)
        for part in parts:
            if part.group() != '':
                part_list.append(Part(part.group(), part.start(), part.end(), y))

        symbols = symbols_re.finditer(line)
        for symbol in symbols:
            if symbol.group() != '':
                symbol_list.append(Item(symbol.group(), symbol.start(), y))
        y += 1

    # Check if there are any PartNumbers adjacent to Symbols.
    schematics = []
    for symbol in symbol_list:
        for part in part_list:
            if part.isNextTo(symbol):
                schematics.append(part)

    total = 0
    for schematic in schematics:
        total += int(schematic.getPartNum())
    print(total)


if __name__ == '__main__':
    main()

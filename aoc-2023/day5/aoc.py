#!/usr/bin/python3

import sys
import re

class Offset():

    def __init__(self, dest, src, offset):
        self.dest = int(dest)
        self.src = int(src)
        self.offset = int(offset)

    def get(self):
        return (self.dest, self.src, self.offset)

    def getDest(self):
        return self.dest

    def getSrc(self):
        return self.src

    def getOffset(self):
        return self.offset

    def getLower(self):
        return self.src

    def getUpper(self):
        return self.src + self.offset

    def __str__(self):
        return '(Destination: %s, Source: %s, Offset: %s)' % (self.dest, self.src, self.offset)


class Map():

    def __init__(self, map_name, map_string):
        self.name = map_name 
        self.seeds = set()
        self.next_map = None
        self.ranges = list() 

        for line in map_string.splitlines():
            unpack = list(map(int, line.split()))
            if len(unpack) > 3:
                # This is how you solve Part 1
#                self.seeds = unpack 

                # This is Part 2

                # TODO: the input comes in pairs of two, not just 4 total... unpack more and add to the setlist

                while unpack:
                    first = unpack[0]
                    off = unpack[1]
                    try:
                        self.seeds.update(set(range(first, first + off)))
                    except:
                        raise RuntimeError("Couldn't build a seed")
                    print(unpack)
                    unpack = unpack[2:]
                print(len(self.seeds))

            else:
                dest = unpack[0]
                src = unpack[1]
                offset = unpack[2]
                self.ranges.append(Offset(dest, src, offset))

    def getName(self):
        return self.name

    def setNextMap(self, map_obj):
        self.next_map = map_obj

    def getNextItem(self, item):
        
#        try:
#           print('I am %s, mapping %s to %s' % (self.name, item, self.next_map.getName()))
#        except AttributeError:
#           print('I am %s, at the bottom of the stack, looking for %s' % (self.name, item))

        for rng in self.get():
            try:
                dest, lower, offset = rng.get()
                dest = rng.getDest()
                lower = rng.getLower()
                upper = rng.getUpper()
                offset = rng.getOffset()
            except AttributeError:
                return self.next_map.getNextItem(item)

#            print('-- Mapping from %s, using lower bound %s & upper bound %s with offset %s' % (item, lower, upper, offset))

            if item >= lower and item < upper:
#                print('-- Found a map! %s maps to %s' % (item, item - lower + dest))
                if self.next_map:
                    return self.next_map.getNextItem(item - lower + dest)
                else:
                    return item - lower + dest
            
            else:
#                print('-- Not Yet.... trying the next range')
                continue
        
        if self.next_map:
#            print('-- Couldn\'t find a map, proceeding with %s' % (item)) 
            return self.next_map.getNextItem(item)
        else:
            return item
    
    def get(self):
        if self.seeds:
            return self.seeds
        else: 
            return self.ranges 

    def getSeeds(self):
        return self.seeds

    def findLocation(self, seed):
        if seed in self.get():
            return self.getNextItem(seed)
        else:
            raise ValueError('That\'s not a Seed I know about')

    def findLowestLocation(self):
        location = None
        for seed in self.getSeeds():
            if location:
                tmp = self.findLocation(seed) 
                if tmp < location:
                    location = tmp
            else:
                location = self.findLocation(seed)
        return location


def main():
    io = open(sys.argv[1], 'r')
    inp = io.read()

    parse = re.compile(r'(?P<name>[a-z -]*):[ \n]?(?P<map>[\d \n]*)\n\n??')

    new_map = None
    old_map = None
    seeds = None

    for mtch in re.finditer(parse, inp):
        map_name = mtch.groupdict()['name']
        items = mtch.groupdict()['map']

        # All the maps go here
        if map_name.endswith('map'):
            new_map = Map(map_name, items.rstrip())
            if old_map:
                old_map.setNextMap(new_map)
                old_map = new_map
        else: # Here are the seeds
#            seeds1 = Map(map_name, items.rstrip('\n'))
            seeds2 = Map(map_name, items.rstrip('\n'))
            old_map = seeds2
   
#    print(seeds2.findLowestLocation())
        
    


if __name__ == '__main__':
    main()

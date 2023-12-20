import sys
from multiprocessing import Pool

io = open(sys.argv[1], 'r')

class Map:

    def __init__(self, instructions, list_of_nodes):
        self.map = dict()
        self.ghosts = []
        self.instructions = instructions
        for node in list_of_nodes:
            node_name = node.getLoc()
            if node_name.endswith('A'):
                self.ghosts.append(node)

            self.map[node.getLoc()] = node
        print(instructions)
        print(self.ghosts)
        print(list_of_nodes)

    def followGhostlyInstructions(self):
        not_done = True
        steps = 0
        current_nodes = self.ghosts

        with Pool(processes=len(self.ghosts)) as pool:
            multiple_results = [pool.apply_async(self.followInstructions, (node, self.instructions)) for node in current_nodes]
            while not_done: 
                print([res.get() for res in multiple_results])


    def followInstructions(self, node, instructions, steps):
        print(node, instructions)

        instruction = instructions[0]
        next_instructions = instructions[1:]

        if node.getLoc().endswith('Z'):
            print('Found the bottom: %s' % (node))
            # TODO: Grab the lock if we found the bottom
            # This will be a signal to check all the other workers
            not_done = False # this is not the right way to do this
            return 1

        #TODO: Add a check on the lock (implemented above) -- 
        #       If the lock is grabbed, that means someone has reached the end
        #       and we need to report back.

        if len(next_instructions) == 0:
            print('Looping back, %s' % (self.instructions))
            instruction = self.instructions[0]
            next_instructions = self.instructions[1:]

        match instruction:
            case 'L':
                print('I\'m at %s, going Left. Next up %s' % (node, next_instructions))
                next_node = self.map[node.getLeft()]
            case 'R':
                print('I\'m at %s, going Right. Next up %s' % (node, next_instructions))
                next_node = self.map[node.getRight()]
        
        return self.followInstructions(next_node, next_instructions) + 1


class Node:

    def __init__(self, loc, left, right):
        self.loc = loc
        self.left = left
        self.right = right

    def getLoc(self):
        return self.loc

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def __str__(self):
        return '\'%s\': (%s, %s)' % (self.getLoc(), self.getLeft(), self.getRight())

    def __repr__(self):
        return self.__str__()


def parse(inp):
    full_input = inp.readlines()
    
    instructions = full_input.pop(0).strip()
    full_input.pop(0)

    nodes = []
    for line in full_input:
        raw = line.strip()
        loc, next_nodes = raw.split(' = ')
        left, right = next_nodes.strip('()').split(', ')
        nodes.append(Node(loc, left, right))

    return instructions, nodes


def main():
    instructions, nodes = parse(io)
    my_map = Map(instructions, nodes)
    my_map.followGhostlyInstructions()

if __name__ == '__main__':
    main()


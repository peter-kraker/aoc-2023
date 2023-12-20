import sys

io = open(sys.argv[1], 'r')

class Map:

    def __init__(self, instructions, list_of_nodes):
        self.map = dict()
        self.instructions = instructions
        for node in list_of_nodes:
            self.map[node.getLoc()] = node
        print(instructions, list_of_nodes)

    # This is the answer to part1

    def followInstructions(self):
        not_done = True
        steps = 0
        current_node = self.map['AAA']
        while not_done:
            for direction in self.instructions:
                match direction:
                    case 'L':
                        if current_node.getLoc() == 'ZZZ':
                            return steps
                        steps += 1
                        current_node = self.map[current_node.getLeft()]
                    case 'R':
                        if current_node.getLoc() == 'ZZZ':
                            return steps
                        steps += 1
                        current_node = self.map[current_node.getRight()]
     


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
    
    instructions = full_input.pop(0)
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

    print(my_map.followInstructions())

if __name__ == '__main__':
    main()


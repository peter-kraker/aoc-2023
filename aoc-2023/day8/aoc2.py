import sys
import os
from multiprocessing import Manager
from multiprocessing import Pool
from multiprocessing import Barrier

io = open(sys.argv[1], 'r')

# Problem: navigate the hauted wasteland. 
# Part 1 - Given a set of instructions and a binary tree, traverse the
#           tree starting at 'AAA' according to the instructions. 
#           Stop when you reach 'ZZZ'.

# Part 2- Traverse multiple paths through a binary tree simultaneously.


# The Map class holds the instructions, and the full list of nodes
class Map:

    # self.map is a dict of Nodes: {'AAA' -> Node('AAA')}
    # self.ghosts is a list of nodes which end in A

    def __init__(self, instructions, list_of_nodes):
        self.map = dict()
        self.ghosts = []
        self.instructions = instructions

        for node in list_of_nodes:
            node_name = node.getLoc()
            if node_name.endswith('A'):
                self.ghosts.append(node)
            self.map[node_name] = node

        print(instructions)
        print(self.ghosts)
        #print(list_of_nodes)

    def followInstructions(self, node, instructions, steps, reports):

        instruction = instructions[0]
        next_instructions = instructions[1:]
        pid = os.getpid()

        #print('%s\tI\'m at %s having gone %s, going %s -- next up %s' % (pid, node, steps, instruction, next_instructions))

        if len(next_instructions) == 0:
            #print('%s\t\tLooping back, %s' % (pid, self.instructions))
            next_instructions = self.instructions

        match instruction:
            case 'L':
                next_node = self.map[node.getLeft()]
            case 'R':
                next_node = self.map[node.getRight()]

        if node.getLoc().endswith('Z'):
            print('%s\tFound the bottom: %s -- it took %s steps' % (pid, node, steps))
            #print('%s\tReports: %s, updating %s with %s' % (pid, reports, pid, steps), flush=True)
            try:
                reports[pid] |= set([steps]) 
                #old_depth = sorted(list(reports[pid]), reverse=True)[0]
            except KeyError:
                reports[pid] = {steps}
            #print('%s\tReports: %s' % (pid, reports))
        #    return (1, next_node, instruction + next_instructions, pid)

        self.followInstructions(next_node, next_instructions, steps + 1, reports)

        #return (self.followInstructions(next_node, next_instructions, steps + 1, reports)[0] + 1, next_node, instruction + next_instructions, pid)

# A node holds itself (e.g. 'AAA') and the left/right links.
# loc, left, right are all Strings.
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
    
    # Pull the instructions off the top.
    instructions = full_input.pop(0).strip()
    full_input.pop(0)

    # Build a list of nodes
    nodes = []
    for line in full_input:
        loc, next_nodes = line.strip().split(' = ')
        left, right = next_nodes.strip('()').split(', ')
        nodes.append(Node(loc, left, right))

    return instructions, nodes

def areWeDone():
    print('Checking if we\'re done: %s' % (reports))
    if intersect != set():
        print('We\'re done! %s' % (intersect))
    else:
        lock.reset()

def followGhostlyInstructions(a_map):
    not_done = True
    current_nodes = a_map.ghosts
    number_of_workers = len(current_nodes)

    with Manager() as manager:
        reports = manager.dict()

        with Pool(processes=number_of_workers) as pool:
            multiple_results = [pool.apply_async(a_map.followInstructions, (node, a_map.instructions, 0, reports)) for node in current_nodes]
            while not_done:
                for res in multiple_results:
                    res.get()
                    #(depth, next_node, instructions, pid) = res.get()
    #                try:
    #                    print('%s\tDepth: %s -- next: %s, %s' % (pid, depth, next_node, instructions), flush=True)
    #                    old_depth = sorted(list(reports[pid]), reverse=True)[0]
    #                    print('%s\tReports: %s, updating %s with %s' % (pid, reports, pid, old_depth + depth), flush=True)
    #                    reports[pid].add(depth + old_depth)
    #                except KeyError:
    #                    print('%s\tAdding %s to reports, with %s steps' % (pid, pid, depth))
    #                    reports[pid] = {depth}
                    print(reports)
                    same = set.intersection(*reports.values())
                if same != set():
                    print('we\'re done! %s' % (same))
                    break
                multiple_results = [pool.apply_async(a_map.followInstructions, (next_node, instructions, depth, reports)) for node in current_nodes]



def main():
    instructions, nodes = parse(io)
    my_map = Map(instructions, nodes)
    followGhostlyInstructions(my_map)


if __name__ == '__main__':
    main()


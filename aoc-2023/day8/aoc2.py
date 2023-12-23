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

    def followInstructions(self, node, instructions, reports, task_id):
        # TODO: Save node, instructions, and taskID in reports -- there's
        #       probably a race condition here, where the number of steps
        #       isn't aligned with the node.
        pid = task_id
        not_done = True

        try:
            steps = sorted(list(reports[pid]), reverse=True)[0]
            #print('%s\tPicking up where we left off: %s steps' % (pid, steps))
        except KeyError:
            steps = 0
            reports[pid] = set()

        while not_done:
            instruction = instructions[0]
            instructions = instructions[1:]

            if len(instructions) == 0:
                instructions = self.instructions

            #print('%s\tI\'m at %s having gone %s, going %s -- next up %s' % (pid, node, steps, instruction, instructions))

            match instruction:
                case 'L':
                    node = self.map[node.getLeft()]
                case 'R':
                    node = self.map[node.getRight()]
            steps += 1
            if node.getLoc().endswith('Z'):
                #print('%s\tFound the bottom: %s -- it took %s steps' % (pid, node, steps))
                #print('%s\tReports: %s, updating %s with %s' % (pid, reports, pid, steps), flush=True)
                try:
                    reports[pid] |= set([steps]) 
                    #old_depth = sorted(list(reports[pid]), reverse=True)[0]
                except KeyError:
                    reports[pid] = {steps}
                #print('%s\tReports: %s' % (pid, reports))
                #return (1, next_node, instruction + next_instructions, pid)
                not_done = False

        return (node, instructions, pid)
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
            while not_done:
                multiple_results = [pool.apply_async(a_map.followInstructions, (node, a_map.instructions, reports, task_id)) for node, task_id in zip(current_nodes, range(number_of_workers))]
                for res in multiple_results:
                    (next_node, instructions, task_id) = res.get()
                    #print(reports)
                    same = set.intersection(*reports.values())
                if same != set():
                    print('we\'re done! %s' % (same))
                    break
                #multiple_results = [pool.apply_async(a_map.followInstructions, (next_node, instructions, reports, task_id)) for node in current_nodes]



def main():
    instructions, nodes = parse(io)
    my_map = Map(instructions, nodes)
    followGhostlyInstructions(my_map)


if __name__ == '__main__':
    main()


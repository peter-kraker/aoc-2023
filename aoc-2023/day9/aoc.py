import sys

io = open(sys.argv[1], 'r')

# Problem: Analyse the changes in values over time... predict the next value in
#           a list of numbers


# Stage class is a linked list of lists. It knows about its own stage e.g.
#   [0 3 6 9 12 15] the stages before and after it, as well as the first
#   and last stages in the 'stack'.

# Possible improvments: 
# Memory effiency -- determine the 'depth' of the stack, trim the lists
# To only the numbers necessary to calculate the last item.
#
# Time Effiency -- Do this with dicts / primitives instead of objects, accessors

class Stage():

    def __init__(self, inp, first_stage=None):
        self.numbers = inp

        # If we call the constructor without a first_stage, then we're the top
        if first_stage is None:
            self.first = self
        else:
            self.first = first_stage

        self.before = None

        if set(inp) == {0}:  
            # If the only thing we have is zeros, we're at the bottom
            self.next = []
            self.last = self 
            self.getFirst().setLast(self) 
        else:
            self.next = self.calculateNext(inp)
            self.getNext().setBefore(self) # Create a back-link

    def extend(self):
        if self.next == []:
            # we're at the bottom, so add a 0 to ourselves, then go up a level
            self.numbers.append(0)
            self.before.extend()
        else:
            # Pull the last item from the next list down, add it to the last
            # item in our list.
            increment = self.getNext()[-1]
            pre = self.numbers[-1]
            # print('Extending %s with %s' % (self.numbers, pre + increment))
            self.numbers.append(pre + increment)
            try:
                self.getBefore().extend()
            except AttributeError:
                # We made it back to the top, and we should be done
                pass

    def calculateNext(self, list_of_numbers):
        numbers = self.numbers.copy()
        next_list = []

        one = numbers.pop(0)
        while numbers:
            two = numbers.pop(0)
            next_list.append(two - one)
            one = two

        return Stage(next_list, self.first)

    def setFirst(self, first_stage):
        self.first = first_stage

    def getFirst(self):
        return self.first

    def setLast(self, last_stage):
        self.last = last_stage

    def getLast(self):
        if self.last:
            return self.last
        else:
            raise ValueError('I don\'t have a last stage yet!')

    def setBefore(self, prior_stage):
        self.before = prior_stage

    def getBefore(self):
        return self.before

    def setNext(self, next_stage):
        self.next = next_stage

    def getNext(self):
        return self.next

    def __str__(self):
        string = ' '.join(map(str, self.numbers)) + '\n'
        try:
            string += (' '.join(map(str, self.next)))
        except TypeError:
            pass 
        return string + '\n' + str(self.getNext())

    def __repr__(self):
        return ' '.join(map(str, self.numbers))

    def __getitem__(self, i):
        return self.numbers[i]
        

def parse(io):
    inp = io.readlines()
    stages = []
    for line in inp:
        number_list = list(map(int, line.strip().split()))
        stages.append(Stage(number_list))
    return stages

def main():
    stages = parse(io)
    total = 0
    for stage in stages:
        stage.getLast().extend()
        total += stage[-1]
    print(total)

if __name__ == '__main__':
    main()


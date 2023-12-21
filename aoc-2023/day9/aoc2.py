import sys

io = open(sys.argv[1], 'r')


class Stage():

    def __init__(self, inp, first_stage=None):
        self.numbers = inp

        if first_stage is None:
            self.first = self
        else:
            self.first = first_stage

        self.before = None

        if set(inp) == {0}:  # If the only thing we have is zeros...
            self.next = []   
            self.last = self 
            self.getFirst().setLast(self) 
        else:
            self.next = self.calculateNext(inp)
            self.getNext().setBefore(self) # Create a back-link

    def extend(self):
        if self.next == []:
            # we're at the bottom, so add a 0, then go up a level
            self.numbers = [0] + self.numbers
            self.before.extend()
        else:
            decrement = self.getNext()[0]
            pre = self.numbers[0]
            print('Extending %s with %s' % (self.numbers, pre - decrement))
            self.numbers = [pre - decrement] + self.numbers
            try:
                self.getBefore().extend()
            except AttributeError:
                # We made it back to the top
                pass

    def __getitem__(self, i):
        return self.numbers[i]

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
        total += stage[0]
    print(total)


if __name__ == '__main__':
    main()


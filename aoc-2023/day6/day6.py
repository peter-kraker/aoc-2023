
import sys
import re
import math

class Race():

  def __init__(self, time, record_distance):
    self.time = time
    self.record_distance = record_distance

  def __init__(self, race_tup):
    self.time = int(race_tup[0])
    self.record_distance = int(race_tup[1])

  def getChargeTimes(self):
    # -time +/- sqrt(time^2-4(-1)(-distance))/(2 (-1))
    a = -1
    b = self.time
    c = -self.record_distance
    smallest_rate = (-b - pow(pow(b, 2) - (4 * a * c), 0.5)) / (2 * a) 
    largest_rate = (-b + pow(pow(b, 2) - (4 * a * c), 0.5)) / (2 * a) 

    return (smallest_rate, largest_rate)

  def getMaxDistance(self):
    time_allowed = self.time

    optimal_rate = time_allowed // 2
    remaining_time = time_allowed - optimal_rate

    if optimal_rate + remaining_time != time_allowed:
      raise ValueError('You did the math wrong')

    distance = optimal_rate * remaining_time
    return distance

  def getNumberOfWins(self):
    lower, upper = self.getChargeTimes()

    return len(range(math.floor(upper), math.ceil(lower)))-1

def parseOne(string):
  return string.split(':')[1].split()

def parseTwo(string):
  return string.split(':')[1].replace(' ','')

def main():
  io = open(sys.argv[1], 'r')
  inp = io.read()

  inp = inp.splitlines()

  times = inp[0]
  distances = inp[1]

  part1_races = []
  for time, distance in zip(parseOne(times), parseOne(distances)):
    part1_races.append((time, distance))

  answer = 1
  for race in part1_races:
    tmp = Race(race)
    answer *= tmp.getNumberOfWins()

  print('Part 1 answer: %s' % (answer))

  part2 = (parseTwo(times), parseTwo(distances))

  print('Part 2 answer: %s' % (Race(part2).getNumberOfWins()))


if __name__ == "__main__":
  main()

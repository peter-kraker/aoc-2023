#!/usr/bin/python3

import sys
import re

io = open(sys.argv[1], "r")
lines = io.readlines()

# Pulling colored cubes out of a bag.
#
# Task: Determine the sum of possible gameIDs when the number of colored
# cubes is constrained (R: 12, G: 13, B: 14)

parse_game = re.compile(r"Game (\d*): (.*)$")
parse_pull = re.compile(r'(?P<number>\d*) (?P<color>red|green|blue)')

maxRed = 12
maxGreen = 13
maxBlue = 14

# Game class stores the gameID and all of it's 'pulls'
class Game:
  maxRed = 12
  maxGreen = 13
  maxBlue = 14

  def __init__(self, game):
    self.game = game
    self.pulls = []

  def addPull(self, pull):
    self.pulls.append(pull)

  def getPulls(self):
    return self.pulls

valid_games = []

for line in lines:
  game = re.match(parse_game, line)
  game_id = game.group(1)
  a_game = Game(game_id)
  valid_game = True

  # Iterate acorss all 'pulls' in a game
  pulls = game.group(2).split("; ")
  for pull in pulls:
    colors = parse_pull.findall(pull)
    for color in colors:
      cube_color = color[1]
      number_of_cubes = int(color[0])

      # Interate through the colors found in a game, check if any exceed the
      # threshold of a valid game.
      match cube_color:
        case "red":
          if number_of_cubes > maxRed:
            valid_game = False
        case "green":
          if number_of_cubes > maxGreen:
            valid_game = False
        case "blue":
          if number_of_cubes > maxBlue:
            valid_game = False

      # At any point, we can quit if the game is invalid
      if valid_game == False:
         #print("Game %s is not valid: %s" % (game_id, pull))
         break

  if valid_game == True:
    valid_games.append(game_id)

total = 0
print("These are the valid games:")
print(valid_games)
for game in valid_games:
  total += int(game)

print(total)

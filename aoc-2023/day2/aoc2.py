#!/usr/bin/python3

import sys
import re

io = open(sys.argv[1], "r")
lines = io.readlines()

parse_game = re.compile(r"Game (\d*): (.*)$")
parse_pull = re.compile(r'(?P<number>\d*) (?P<color>red|green|blue)')

power_of_game = []

for line in lines:
  game = re.match(parse_game, line)

  highest_red = 0 
  highest_green = 0
  highest_blue = 0

  pulls = game.group(2).split("; ")
  for pull in pulls:
    colors = parse_pull.findall(pull)

    for color in colors:
      cube_color = color[1]
      number_of_cubes = int(color[0])
      match cube_color:
        case "red":
          if number_of_cubes > highest_red:
            highest_red = number_of_cubes
        case "green":
          if number_of_cubes > highest_green:
            highest_green = number_of_cubes
        case "blue":
          if number_of_cubes > highest_blue:
            highest_blue = number_of_cubes
  power_of_game.append(highest_red * highest_green * highest_blue) 

answer = 0
for game in power_of_game:
  answer += int(game)

print(answer)

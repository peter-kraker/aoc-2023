import sys

io = open(sys.argv[1], "r")
inp = io.readlines()

linenums = []

# Task: Add up the first and last number in a line
for line in inp:
  first = 0
  last = 0
  seen_num = False

  # Go through the characters, if they can be cast to an int, they're a number!
  # if not, go to the next one.
  #
  # Possible improvement: once we find the first number, flip the line, and
  # go backwards.
  for char in line:
    try:
      if seen_num == False:
        first = int(char)
        seen_num = True
      last = int(char)
    except ValueError:
      continue
  linenums.append(int(str(first)+str(last)))

total = 0
for num in linenums:
  total += num

print(total)
io.close()

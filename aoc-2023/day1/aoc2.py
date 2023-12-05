import sys

io = open(sys.argv[1], "r")
inp = io.readlines()

alphadict = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

def getPosition(tup):
  return tup[1]

def number(line):
  first_digit = ()
  first_alpha = ()
  last_digit = ()
  last_alpha = ()

  # Get the first and last digits in the line, stop after finding each.
  # Save the numbers and their position in a tuple.
  pos = -1
  for char in line:
    pos += 1
    if char.isdigit():
      first_digit = (char, pos)
      break

  pos = len(line)
  for char in line[::-1]:
    pos -= 1
    if char.isdigit():
      last_digit = (char, pos)
      break
  
  # Look for the first and last alpha characters ("one", "two", etc.)
  # 
  # Search the line for each number from one to ten, save the results and their
  # positions in a tuple. (e.g. 
  #  
  # In order to catch duplicates (e.g. nineninenine), search for the first
  # and last instance by using String.find() and String.rfind().
.
  forward_alphas = []
  reverse_alphas = []
  for alpha in alphadict.keys():
    if alpha in line:
      # Convert the alpha characgter to its digit equivalent "one" -> "1"
      forward_alphas.append((alphadict[alpha], line.find(alpha)))
      reverse_alphas.append((alphadict[alpha], line.rfind(alpha)))
  forward_alphas.sort(key=getPosition)
  reverse_alphas.sort(key=getPosition, reverse=True)
  

  # Figure out which comes first and last, the digits, or the alpha characters
  first = 0
  last = 0

  try:
    first_alpha = forward_alphas[0]
    last_alpha = reverse_alphas[0]
  except IndexError: 
  # If we get an IndexError here, there werent' any alphas, so we can just use
  # the digits
    first = first_digit[0]
    last = last_digit[0]
    return int(first + last)

  # Compare the positions of the digits to the alphas, pick the correct one.
  try:
    if getPosition(first_digit) < getPosition(first_alpha):
      first = first_digit[0]
    else: 
      first = first_alpha[0]

    if getPosition(last_digit) > getPosition(last_alpha):
      last = last_digit[0]
    else:
      last = last_alpha[0]
  except IndexError:
    # If we get an IndexError here, there were no digits, so just use the alphas
    first = first_alpha[0]
    last = last_alpha[0]
    
  return int(first + last)

# Add everything up
total = 0
for line in inp:
  total += number(line)

print(total)
io.close()

import sys

io = open(sys.argv[1], "r")
inp = io.readlines()

linenums = []

for line in inp:
  first = 0
  last = 0
  seen_num = False
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

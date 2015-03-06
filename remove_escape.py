import sys
s=sys.stdin.readlines()
for line in s:
  sentence=""
  temp=0
  for i in range(0,len(line)-1):
    if line[i]=="\\":
      continue
    sentence+=line[i]
  print sentence
    

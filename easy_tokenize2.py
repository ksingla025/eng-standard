#!/usr/bin/python
import sys
import string

def ambiguated_output(list_of_tokens):
  l=[]
  for word in list_of_tokens:    # list of tokens is the double list
    s='^'
    j='/'.join(word)
    s=s+j+'$'
    l+=[s]
  return l


def disambiguated_output(line):
  x=line[1:-2]   # ^ and $ symbols are ommitted
  tokens="/".split(x)
  return x


def detect_cat(d):
  if d=="#" or d=="@" or d=="'" or d=="<" or d==">" :
    return 1
  if d in [",",".","!","?"]:
    return 0
  else:
    return 1
  
  
def main():
  s=sys.stdin.readlines()
  for line in s:
    flag=detect_cat(line[0])
    sentence=""
    temp=0
    flag_link=0
    for i in range(0,len(line)):
      if i<=temp:
        continue
      if line[i]=="\\":
        temp=i+1
        sentence+=line[i]+line[i+1]
        continue
      if flag_link==1:
        if line[i]==">":
          flag_link=0
          sentence+=">"
          continue
        sentence+=line[i]
        continue
      if line[i]=="<":
        flag_link=1
        sentence+=line[i]
        continue
      if detect_cat(line[i])==1 and flag==0:   # now the char are seen
        flag=1
        sentence+=" "+line[i]
        continue
      if detect_cat(line[i])==0 and flag==1:
        flag=0
        sentence+=" "+line[i]
        continue
      sentence+=line[i]
    print sentence[:-1]
      
if __name__=="__main__":
  main()  


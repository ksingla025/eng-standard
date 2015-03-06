#!/usr/bin/python
import sys
import re
def ambiguated_output(list_of_tokens):
  dl=[]
  for word_token in list_of_tokens:
    s='^'+word_token[0]+"/"
    l=[]
    for word in word_token[1:]:
      if word in l:
        continue
      else:
        l+=[word]
    j='/'.join(l)
    s=s+j+'$'
    dl+=[s]
  return dl
# returns disambiguated all the double list of tokens in a line
def disambiguated_output_line(line):
  dl=[]
  tokens=[]
  word=""
  flag=0
  temp=0
  x=line
  new=[]
  for i in range(0,len(x)-1):
    if i<temp:
      continue
    if x[i]=="^":
      word=""
      continue
    if x[i]=="$":
      tokens+=[word]
      new+=[tokens]
      tokens=[]
      continue
    if x[i]=="\\":
      word+=x[i]+x[i+1]
      temp=i+2
      continue
    if x[i]=="/":
      tokens+=[word]
      word=""
      continue
    word+=x[i]
  return new

def main():
  s=sys.stdin.readlines()
  for line in s:
    dl=disambiguated_output_line(line)
    new_sent=[]
    for word_tokens in dl:
      best_word=word_tokens[-1]
      if best_word[0]=="<" and best_word[-1]==">":
        new_sent+=[word_tokens[-1][1:-1]]
        continue
      new_sent+=[word_tokens[-1]]
    print " ".join(new_sent)

if __name__=="__main__":
  main()

#!/usr/bin/python

import sys
import re

#function below
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



def replace_hashtags(line):
  flag=0
  new=""
  if line[0]=="#":
    return "<"+line+">"
  else:
    return line
  

def main():
  s=sys.stdin.readlines()
  dl=[]
  new=[]
  for line in s:
    dl=disambiguated_output_line(line)
    new=[]
    for word_token in dl:
      x=[]
      word=replace_hashtags(word_token[-1])
      x=word_token+[word]
      new+=[x]
    print " ".join(ambiguated_output(new))

if __name__=="__main__":
  main()

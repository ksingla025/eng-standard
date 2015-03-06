#!/usr/bin/python
########Author Akshay Minocha ( ksnmi | minocha )##############
########mailto:akshayminocha5@gmail.com########################

import pickle
#substitution list
import sys
temp=open("temp_language").read().split()[0]
d=pickle.load(open("abbr_dict_"+temp))
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
  global d
  text=sys.stdin.readlines()
  for line in text:
    x=disambiguated_output_line(line)
    new_sent=[]
    for word_token in x:
      word=word_token[-1]
      if word[0]=="<" and word[-1]==">":
        new_sent+=[word_token]   #print " ".ambiguated_output(word_token)
        continue
      if word.lower() in d:
        new_word=d[word.lower()]
        new_sent+=[word_token+[new_word]]
        continue
      else:
        new_sent+=[word_token]
    print " ".join(ambiguated_output(new_sent))
  
if __name__=="__main__":
  main()

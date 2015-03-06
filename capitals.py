#!/usr/bin/python

import sys
import string
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
  some_known={"i":"I","i'd":"I'd","i've":"I've","i'm":"I'm","i'll":"I'll"}
  s=sys.stdin.readlines()
  sent_end=['!','?','.']
  for line in s:
    x=disambiguated_output_line(line)
    new_sent=[]
    for word_tokens in range(0,len(x)):
      best_word=x[word_tokens][-1]
      if best_word[0]=="<" and best_word[-1]==">":
        new_sent+=[x[word_tokens]]
        continue	
      if word_tokens==0:
        if best_word[0].capitalize()!=best_word[0]:    # not capital
          new_sent+=[x[word_tokens]+[best_word.capitalize()]]
          continue
        else:
          new_sent+=[x[word_tokens]]
          continue
      if best_word.lower() in some_known:
        new_sent+=[x[word_tokens]+[some_known[best_word.lower()]]]
        continue
      if x[word_tokens-1][-1][0] in sent_end:
        if best_word[0].capitalize()!=best_word[0]:    # not capital
          new_sent+=[x[word_tokens]+[best_word.capitalize()]]
          continue
        else:
          new_sent+=[x[word_tokens]]
          continue
      else:
        new_sent+=[x[word_tokens]]
        continue
    print " ".join(ambiguated_output(new_sent))
          
if __name__=="__main__":
  main()

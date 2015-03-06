#!/usr/bin/python
##########Author:Akshay Minocha | ksnmi #########
##########mailto:akshayminocha5[at]gmail.com#####

import sys
import pickle

#pickle because the list is too small. This is a universal list independent of the language
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
  emo=pickle.load(open("emoticons_pickle"))
  lines=sys.stdin.readlines()
  for line in lines:
    x=disambiguated_output_line(line)
    new_sent=[]
    for word_token in x:
      word=word_token[-1]
      if word in emo:
        new_word="<"+word+">"
        new_sent+=[word_token+[new_word]]
        continue
      else:
        new_sent+=[word_token]
    print " ".join(ambiguated_output(new_sent))
    #new_content=ambiguated_output(x)
    #print " ".join(new_content)
    #new_content=" ".join(x)
    #print new_content
  
if __name__=="__main__":
  main()

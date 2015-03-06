#!/usr/bin/python
#This is the script which works for the text written in English or INTENDED to be written in English. This text may or may not be grammatically correct. Our aim is to normalise the repititions in the word.
########Author Akshay Minocha ( ksnmi | minocha )##############
########mailto:akshayminocha5@gmail.com########################
import sys
import itertools
import string
import pickle
# this script takes in from stdin normal input.. not line per token format

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

def check_repitition(word):
  # returns 1 if the number of characters is >=3 
  # returns 0 if it thinks the word has non repititive characters (otherwise)
  punc=string.punctuation
  if word[0] in punc:
    return 0
  flag_count=0
  flag=''
  for i in range(0,len(word)):
    if i==0:
      flag=word[0]
      flag_count=1
      continue
    else:
      if word[i]==flag:
        if word[i] in punc:
          flag_count=0
        flag_count+=1
        if flag_count>2:
          return 1
      else:
        flag=word[i]
        flag_count=1
  return 0
 
def generate_variations(word):
  flag_count=0
  flag=''
  temp=word[0]
  list_of_rep=[]
  for i in range(0,len(word)):
    if i==0:
      flag=word[0]
      flag_count=1
      continue
    else:
      if word[i]==flag:
        flag_count+=1
        if flag_count>3:
          continue
        if flag_count>2:
          list_of_rep+=[len(temp)-2]
          continue
        else:
          temp+=word[i]
      else:
        flag=word[i]
        flag_count=1
        temp+=word[i]
  return (temp,list_of_rep)
 
def generate_all_variations(tuple_info):
  #0th -> original candiate normalised( 1stage )
  # all repititions which are detected earlier ( have either 1 or 2 repititions as the final output of this script)
  length=len(tuple_info[1])  # all the index positions where the repititions > 3 were made
  all_words=[]
  list_of_index=tuple_info[1]
  word=tuple_info[0]
  for x in map(''.join, itertools.product('01', repeat=length)):
    #print word
    temp=word[:list_of_index[0]+1]
     
    flag=list_of_index[0]+2
    for i in range(0,len(x)):
      if x[i]=="1":
        temp+=word[list_of_index[i]]
      if i+1<len(x):
        temp+=word[flag:list_of_index[i+1]+1]
        flag=list_of_index[i+1]+2
      else:
        temp+=word[flag:]
    all_words+=[temp]
  return all_words
 
def main():
  #wordlist=pickle.load(open("wordlist_dic"))
  input1=sys.stdin.readlines()
  #output format of the first stage will be 
  #^original_word/candidate1/candidate2/candidate3 and so on$
  list_of_tokens=[]
  lang=open("temp_language").read().split()[0]
  english_wordlist=pickle.load(open("wordlist_dic_"+lang))
   
  for line in input1:
    x=disambiguated_output_line(line)
    new_sent=[]
    for word_tokens in x:
      word=word_tokens[-1]
      if word[0]=="<" and word[-1]==">":
        new_sent+=[word_tokens]
        continue
      if check_repitition(word)==1:
        temp=[]
        gv=generate_variations(word)
        temp=[word]
        for j in generate_all_variations(gv):
          temp+=[j]
        flag=0
        for j in temp:
          if j.lower() in english_wordlist:
            new_sent+=[word_tokens+[j]]
            flag=1
            break
        if flag==0:
          new_sent+=[word_tokens]
      else:
        new_sent+=[word_tokens]   #temp=[word]
    print " ".join(ambiguated_output(new_sent))
   
   
if __name__=="__main__":
  main()


#!/usr/bin/python
import sys
import pickle
#import MicrosoftNgram as MNgr

lang=open("temp_language").read().split()[0]

wordlist=pickle.load(open("wordlist_dic_"+lang))
trigram_data=pickle.load(open("trigrams_"+lang))
bigram_data=pickle.load(open("bigrams_"+lang))
d1=pickle.load(open("apostrophe_"+lang))
d2=pickle.load(open("apostrophe_error_"+lang))

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



#all lower case trigrams and bigrams in the dict
def check_trigram(trigram,w1,w2):
  global trigram_data
  t=trigram.lower().split()
  seq1=" ".join(t)
  seq2=w2+" "+t[1]+" "+t[2]
  #seq1_num=MNgr.lookup.GetJointProbability(seq1)
  #seq2_num=MNgr.lookup.GetJointProbability(seq2)
  #print seq1, seq1_num
  #print seq2, seq2_num
  if seq1 in trigram_data and seq2 in trigram_data:
    if trigram_data[seq1]<=trigram_data[seq2_num]:
      return w2
    else:
      return w1
  if seq1 in trigram_data:
    return w1
  if seq2 in trigram_data:
    return w2
  return w1

#all lower case trigrams and bigrams in the dict
def check_bigram(bigram,w1,w2):
  global bigram_data
  t=bigram.lower().split()
  seq1=" ".join(t)
  seq2=w2+" "+t[1]
  if seq1 in bigram_data and seq2 in bigram_data:
    if bigram_data[seq1]<=bigram_data[seq2_num]:
      return w2
    else:
      return w1
  if seq1 in bigram_data:
    return w1
  if seq2 in bigram_data:
    return w2
  return w1


def function2(word,sent,index):
  global wordlist
  global d2
  if word.lower() in d2:
    if word.lower() in wordlist:  # ambiguated words like he'll she'll
      if index+3<=len(sent):
        trigram_old=word.lower()+" "+sent[index+1][-1].lower()+" "+sent[index+2][-1].lower()
        #print trigram_old
        ret=check_trigram(trigram_old,word.lower(),d2[word.lower()])
        return ret
      elif index+2<=len(sent):
        bigram_old=word.lower()+" "+sent[index+1][-1].lower()
        ret=check_bigram(bigram_old,word.lower(),d2[word.lower()])
        return ret
    else:
      return d2[word.lower()]
  else:
    return word
 
def main():
  s=sys.stdin.readlines()
  global d1
  global d2
  for line in s:
    #sentence=[]   # double list
    sentence=disambiguated_output_line(line)
    #print sentence, "sentence"
    count=0
    new_sent=[]   # check here
    for word_token in sentence:
      best_word=word_token[-1] 
      if best_word[0]=="<" and best_word[-1]==">":
        new_sent+=[word_token]
        continue 
      if best_word=="'":
        new_sent+=[word_token+[best_word]]
        count+=1
        continue
      if "'" in best_word:
        if best_word.lower() in d1:
          new_sent+=[word_token+[best_word]]
          count+=1
          continue
        else:
          nword="".join(best_word.split("'"))
          NW=function2(nword, sentence, count)   # should handle the wrong apostrophe here.. have to check like do'nt Im'
          new_sent+=[word_token+[NW]]
          count+=1
          continue
      else:
        NW=function2(best_word, sentence, count)   # words with no apostrophe
        if NW==None:
          new_sent+=[word_token+[best_word]]
          count+=1
          continue
        new_sent+=[word_token+[NW]]
        count+=1
    #print new_sent
    print " ".join(ambiguated_output(new_sent))


if __name__=="__main__":
  main()  

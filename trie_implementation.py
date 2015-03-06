#!/usr/bin/python

#improving shorten abbreviations, short lingo

import string 
import sys
import pickle
#!/usr/bin/env python
b=[]                              # A container that would hold suggestions 


class Trie():

    def __init__(self):
        self.root = {}
	self.val=0               # To store count of each character's occurance in a particular path
	self.depth=0             # depth of each character in a particular path

#--------------------------------------------------------------------------------------#
#            Internal Function that returns bool true if key exists in the trie        #
#		and false otherwise , along with the count , it occurs                 # 

    def __contains__(self, word):
	word=word+'$'
        curr_node = self.root
	no=len(word)
        for char in word:
	    no-=1
            try:
		if no==0:
		      return [True,curr_node[word[-1]].val]
                curr_node = curr_node[char].root
            except KeyError:
                return [False,0]
	if None in curr_node:
	       return [True,curr_node[word[-1]].val]
	else :
	       return [False,0]

#----------------------------------------------------------------------------------------#
#         Internal Function to insert a word into the trie 			         #

    def __add__(self, word):
	word=word+'$'
        curr_node = self.root
	no=len(word)
	counter=0
        for char in word:
		counter+=1
		try:
			curr_node[char].val+=1
			curr_node[char].depth=counter
			curr_node = curr_node[char].root
	   	except KeyError:
			curr_node[char] = Trie()
                	curr_node[char].val+=1
			curr_node[char].depth=counter
                	curr_node = curr_node[char].root
        curr_node[None] = word

#---------------------------------------------------------------------------------------#

    def update(self, words):
#              A Function to update tree with multiple words at once                    #
        for word in words:
            self.add(word)

   
#---------------------------------------------------------------------------------------#
#           Internal Function to print trie in indented form (calls ptrie)              #

    def __ptrie__(self):
	    temp = self.root.keys()
	    temp.sort()
	    for i in temp :
		    if(i!=None):
			    indent=self.root[i].depth
			    print '| '*indent+i
			    curr_node=self.root[i]
			    if(len(curr_node.root)!=0):
				    curr_node.__ptrie__()

#---------------------------------------------------------------------------------------#
# 			Internal functions for remove operation                         #

    def __reduces__(self, word):
	word=word+'$'
        curr_node = self.root
        for char in word:
		try:
			if(curr_node[char].val>0):
				curr_node[char].val-=1
			curr_node = curr_node[char].root
	   	except KeyError:
			return -1
        curr_node[None] = word 


    def __initdel__(self,key):
	self.__deletes__(key+'$')


    def __deletes__(self,key):
	head = key[0]
	if head in self.root:
		try:
	    		node=self.root[head]
	    	except KeyError:
	    		return 'Not Found'
	if len(key)>1:
		remains=key[1:]
	    	node.__deletes__(remains)
	if node.val==0 :
		del self.root[head]

#----------------------------------------------------------------------------------------------#
#                Internal Functions for obtaining suggestions                                  #

    a=[]
    def __collectsuggestions__(self,word):
	    for char in self.root.keys():
		    if self.root[char].root.has_key('$') :
		    	    self.a.append(word+char)
		#	    print self.a
		    if char !=None and char !='$':
		    	    self.root[char].__collectsuggestions__(word+char)
	    return self.a

    def __suggests__(self,key,x=''):
	    global b
	    head=key[0]
            #b=[]
            #print b, "after removing"
	    x=x+head
	    if head in self.root:
			    curr_node=self.root[head]
			    if len(key)>1:
		    		    curr_node.__suggests__(key[1:],x)
			    else :
				  b=curr_node.__collectsuggestions__(x)

#--------------------------------------------------------------------------------------------#
#                      Functions intended to be called by user                               #

    def insert(self,word):
	    self.__add__(word)
	    #print str(self.__contains__(word)[1])


    def remove(self,word):
	    if self.__contains__(word)[0]:
	    	self.__reduces__(word)
	    	self.__initdel__(word)
		#print self.__contains__(word)[1]


    def ptrie(self):
	    print 'root'
	    self.__ptrie__()


    def search(self,word):
	counter=0
	global b
	a= self.__contains__(word)
        length=len(b)
	if a[0]:
		return [1,[a[1]]]
	else :
                #b=[]
		self.__suggests__(word)
                b+=[word]
                #print b, "there is the b"
                return [0,b[length:]]

#--------------------------------------------------------------------------------------------------#
lang=open("temp_language").read().split()[0]
unigram=pickle.load(open("unigram_count_"+lang))
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

def check_unigram(tokens):
  g={}
  #print tokens, "unigram check"
  for i in tokens:
    i=i.lower()
    if i in unigram:
      g[i]=unigram[i]
  if len(g)==0:
    #print len(tokens)
    return tokens[-1]
  else:
    maximum=0
    element=-1
    for i in g.keys():
      if g[i]>maximum:
        maximum=g[i]
        element=tokens.index(i)
    return tokens[element]

def main():
  global lang
  s=pickle.load(open("wordlist_dic_all_words_"+lang))
  t=Trie()
  for i in s.keys():
    t.insert(i.lower())
  input=sys.stdin.readlines()
  for line in input:
    dl=disambiguated_output_line(line)
    new_sent=[]
    for word_tokens in dl:
      best_word=word_tokens[-1]
      if best_word[0]=="<" and best_word[-1]==">":
        new_sent+=[word_tokens]
        continue
      if best_word[0] in string.punctuation:
        new_sent+=[word_tokens]
        continue
      x=t.search(best_word.lower())
      if x[0]==1:
        new_sent+=[word_tokens]
        continue
      else:
        if len(x[1])>0:
          pr=check_unigram(x[1])
          if best_word[0]!=best_word[0].capitalize():
            new_sent+=[word_tokens+[pr]]
            continue
          else:
            new_sent+=[word_tokens+[pr.capitalize()]]
            continue
    print " ".join(ambiguated_output(new_sent))
              
          


if __name__=="__main__":
        main()

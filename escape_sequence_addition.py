#!/usr/bin/python
########author: Akshay Minocha############
########mailto:akshayminocha5@gmail.com###
#In accordance with the Apertium stream format ... http://wiki.apertium.org/wiki/Apertium_stream_format
import re
import sys


def hashtag_hyperlink(word):
  if word[0]=="#" or word[:4]=="http":
    return "<"+word+">"
  return word

def main():
  text=sys.stdin.readlines()
  for line in text:
    x=re.sub('\@',r'\@',line)
    x=re.sub('\^','\^',x)
    x=re.sub('\$','\$',x)
    x=re.sub('\<','\<',x)
    x=re.sub('\>','\>',x)
    #x=re.sub('\}','\}',x)
    #x=re.sub('\{','\{',x)
    x=re.sub('/','\/',x)
    #x=re.sub(r'*','\*',x)
    p=[]
    for i in x.split():
      p+=[hashtag_hyperlink(i)]
    print " ".join(p)
  
if __name__=="__main__":
  main()

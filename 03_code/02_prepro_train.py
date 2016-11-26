import gensim
import unicodedata
import pandas as pd
import sys
import csv
import os
import nltk
import io


os.chdir('/Volumes/Seagate Backup Plus Drive/NLP/NER_Spectral/02_clean_data/')

tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

fname = "Word_embedding_Default/vocab.txt"
read_file=open(fname,'r')
vocab= [line.strip() for line in read_file]

fname = "train.txt"
read_file=io.open(fname,'r', encoding = 'utf-8')
line_aux = ""
p = 0
for line in read_file:
  aux=line.strip().split(" ")

  if len(aux)>1 and aux[1]!="O":
    line_aux = line_aux + " " + aux[0] + "(" + aux[1] + ")"
    #line_aux = line_aux + " " + aux[0]
  else:
    line_aux = line_aux + " " + aux[0]
  if p == 5000:
    break
  p +=1

sentence_line = tokenizer.tokenize(line_aux[1:10000])
print(sentence_line )
#print(sentence_line)
#print '\n-----\n'.join(tokenizer.tokenize(line_aux))

#split = " ".join(split)
#split = "Gobierno para negociar un aumento de los cr\'e9ditos concedidos a los campesinos ya asentados . Gobierno para negociar un aumento de los cr\'e9ditos concedidos a los campesinos ya asentados."

#data

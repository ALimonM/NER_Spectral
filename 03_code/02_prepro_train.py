import gensim
import unicodedata
import pandas as pd
import sys
import csv
import os
import nltk
import io
import string
import re
from sys import exit

os.chdir('/Volumes/Seagate Backup Plus Drive/NLP/NER_Spectral/02_clean_data/')

tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')

fname = "Word_embedding_Default/vocab.txt"
read_file=open(fname,'r')
vocab= [line.strip() for line in read_file]

fname = "word_embedding_input.txt"
read_file=io.open(fname,'r', encoding = 'utf-8')
line_aux = ""
p = 0
for line in read_file:
  aux=line.strip().split(" ")
  #aux[0] = re.sub('[0-9]+', 'DIGITO', aux[0])
  if len(aux)>1 and aux[1]!="O":
    #line_aux = line_aux + " " + aux[0] + "(" + aux[1] + ")"
    line_aux = line_aux + " " + aux[0].replace(".", "")
  else:
    line_aux = line_aux + " " + aux[0]
sentence_line = tokenizer.tokenize(line_aux)
print(len(sentence_line))
thefile = open('word_embedding_p.txt', 'w')
exclude = set(string.punctuation)

for item in sentence_line:

  if len(item.split(" "))>10:
    pattern ='(?P<order>[0-9\.\,]+)'
    item = re.sub(pattern, "DIGITO",item)
    item = ''.join(ch for ch in item if ch not in exclude)
    thefile.write("%s\n" % item.encode('utf-8'))

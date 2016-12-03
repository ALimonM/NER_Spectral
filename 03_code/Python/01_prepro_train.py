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

#Convert train and text 

os.chdir('/Volumes/limoncito/NLP/NER_Spectral/')



train=io.open("01_raw_data/train.txt",'r', encoding = 'utf-8')
evaluation = io.open("01_raw_data/validation.txt",'r', encoding = 'utf-8')

lines = []
for line in train:
  lines.append(line)
for line in evaluation:  
  lines.append(line) 


line_aux = ""
p = 0
for line in lines:
  aux=line.strip().split(" ")
  if len(aux)>1 and aux[1]!="O":
    line_aux = line_aux + " "+ aux[0].replace(".", "")  
  else:
    line_aux = line_aux + " " + aux[0]


tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')    
sentence_line = tokenizer.tokenize(line_aux)

thefile = open('02_clean_data/training_to_sentece.txt', 'w')
exclude = set(string.punctuation)

for item in sentence_line:

  if len(item.split(" "))>10:
    pattern ='(?P<order>[0-9]+)'
    item = re.sub(pattern, "DIGITO",item)
    item = ''.join(ch for ch in item if ch not in exclude)
    pattern = 'DIGITO[\s]+DIGITO'
    for i in range(5):
      item = re.sub(pattern, "DIGITO ",item)
    pattern = 'DIGITODIGITO'
    for i in range(5):
      item = re.sub(pattern, "DIGITO",item)  
    thefile.write("%s\n" % item.encode('utf-8'))
   
    

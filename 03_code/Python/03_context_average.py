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
import codecs

#Convert train and text 

#/home/mc3784/OPTIMIZATION/NER_Spectral/03_code/
train_path = "/Volumes/limoncito/NLP/NER_Spectral/01_raw_data/train.txt"
eval_path = "/Volumes/limoncito/NLP/NER_Spectral/01_raw_data/validation.txt"
output_path = '/Volumes/limoncito/NLP/NER_Spectral/02_clean_data/context_prep.txt'



def replace_digit(item):
    pattern = 'DIGITO\sDIGITO'
    for i in range(10):
      item = re.sub(pattern, "DIGITO ",item)
    pattern = 'DIGITO[\.\,\-\s]DIGITO'
    for i in range(10):
      item = re.sub(pattern, "DIGITO",item)
    pattern = 'DIGITO[\s]+DIGITO'
    for i in range(10):
      item = re.sub(pattern, "DIGITO",item)
    return item 



train=io.open(train_path,'r', encoding = 'utf-8')
evaluation = io.open(eval_path,'r', encoding = 'utf-8')

lines = []
for line in train:
  lines.append(line)
for line in evaluation:  
  lines.append(line) 

line_aux = ""
p = 0
named_entity = []
pattern ='[0-9]+'
sentence_line=[]
for line in lines:
    aux=line.strip().split(" ")
    if len(aux)==1:
        sentence_line.append(replace_digit(line_aux))
        line_aux = ""        
    aux[0] = re.sub(pattern, "DIGITO",aux[0])
    if len(aux)>1 and aux[1]!="O":
        if aux[1][0]=="B": 
            line_aux = line_aux + " " + "XXXAA" + aux[1][2:5] + aux[0].replace(".", "") + "XXXAA"
        else:
            if line_aux[-5:] == "XXXAA" and aux[1][0]=="I":
                line_aux = line_aux[:-5] + " " + aux[0].replace(".", "")  + "XXXAA"
    else:
        line_aux = line_aux + " " + aux[0]

    
    
#tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')    
#sentence_line = tokenizer.tokenize(line_aux)

thefile = open(output_path, 'w')
exclude = set(string.punctuation)

for item in sentence_line:
    pattern ='(?P<order>[0-9]+)'
    item = re.sub(pattern, "DIGITO",item)
    item = ''.join(ch for ch in item if ch not in exclude)
    pattern = 'DIGITO[\s]+DIGITO'
    for i in range(5):
      item = re.sub(pattern, "DIGITO ",item)
    pattern = 'DIGITODIGITO'
    for i in range(5):
      item = re.sub(pattern, "DIGITO",item)
    item = item.replace("  "," ")
    item = item.strip()
    if len(item.split(" "))>10:
        thefile.write("%s\n" % item.encode('utf-8'))

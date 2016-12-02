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

#os.chdir('/Volumes/limoncito/NLP/NER_Spectral/')

context_words = 2

train=io.open("train.txt",'r', encoding = 'utf-8')
evaluation = io.open("validation.txt",'r', encoding = 'utf-8')

lines = []
for line in train:
  lines.append(line)
for line in evaluation:  
  lines.append(line) 
print(1)

line_aux = ""
p = 0
named_entity = []
print(len(lines))
for line in lines:
  aux=line.strip().split(" ")
  if len(aux)>1 and aux[1]!="O":
    if aux[1][0]=="B": 
      line_aux = line_aux + " " + "XXXAA" + aux[1][2:5] + aux[0].replace(".", "") + "XXXAA"
    else:
      if line_aux[-5:] == "XXXAA" and aux[1][0]=="I":
        line_aux = line_aux[:-5] + " " + aux[0].replace(".", "")  + "XXXAA"
  else:
    line_aux = line_aux + " " + aux[0]
print(2)

tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')    
sentence_line = tokenizer.tokenize(line_aux)
exclude = set(string.punctuation)

sentence_line_f= []
for item in sentence_line:
  if len(item.split(" "))>10:
    pattern ='(?P<order>[0-9]+)'
    item = re.sub(pattern, "DIGITO",item)
    item = ''.join(ch for ch in item if ch not in exclude)
    pattern = 'DIGITO\sDIGITO'
    for i in range(5):
      item = re.sub(pattern, "DIGITO ",item)
    pattern = 'DIGITODIGITO'
    for i in range(5):
      item = re.sub(pattern, "DIGITO",item)
    sentence_line_f.append(item.replace("  "," ").strip())

#sentence_line_f =  sentence_line_f

context_name_ent = []
named_entity = []
tag = []
counter = 0
for item in sentence_line_f:
    list_entity = re.findall(r'XXXAA(.*?)XXXAA',item)
    for element in list_entity:
        named_entity.append(element)
        item = item.replace(element, element[3:])
    while len(item.split("XXXAA", 2)) > 1:
      item_list = item.split("XXXAA", 2)
      item_list = filter(None, item_list)
      if len(item_list) == 2:
        if item[:5] == "XXXAA":
          aux_list= item_list[1].replace("XXXAA", "").split(" ")
          aux_list = filter(None, aux_list)        
          context_name_ent.append(aux_list[:context_words*2])
        else:
          aux_list= item_list[0].replace("XXXAA", "").split(" ")
          aux_list = filter(None, aux_list)        
          context_name_ent.append(aux_list[-context_words*2:])
        item = item_list[0] + item_list[1]
      elif len(item_list)>2:
        aux_list= item_list[0].replace("XXXAA", "").split(" ")
        aux_list = filter(None, aux_list)
        aux_list_1= item_list[2].replace("XXXAA", "").split(" ")
        aux_list_1 = filter(None, aux_list_1)
        n  = len(aux_list)
        m = len(aux_list_1)
        if n>=context_words and m>= context_words:
          context_name_ent.append(aux_list[-context_words:] + aux_list_1[:context_words])          
        elif n< context_words and (m >= (context_words*2 -n)):
          context_name_ent.append(aux_list + aux_list_1[:(context_words*2-n)] )
        elif m< context_words and (n >= (context_words*2 -m)):
          context_name_ent.append( aux_list[:(context_words*2-m)] + aux_list_1 )          
        item = item_list[0] + item_list[1] + item_list[2]


thefile = open('context_words_2.txt', 'w')
i = 0
for item in context_name_ent:
    for el in item:
       thefile.write("%s\t" % el.encode('utf-8'))
    thefile.write("\n")

thefile = open('02_clean_data/named_entity_2.txt', 'w')
for item in named_entity:
    thefile.write("%s\t" % item[:3].encode('utf-8'))
    thefile.write("%s\n" % item[3:].encode('utf-8'))


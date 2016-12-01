import unicodedata
import pandas as pd
import os
import io
import re
import string

os.chdir('/Volumes/Seagate Backup Plus Drive/NLP/NER_Spectral/')

vocab=io.open("02_clean_data/Word_embedding_Default/vocab.txt",'r', encoding = 'utf-8')
vocab=io.open("02_clean_data/entities.txt",'r', encoding = 'utf-8')


lines = []
for line in train:
  lines.append(line)
for line in evaluation:  
  lines.append(line) 



entity = []
named_entity = []


exclude = set(string.punctuation)
pattern ='(?P<order>[0-9\.\,]+)'
aux_list=[]
for line in lines:
  aux=line.strip().split(" ")
  aux[0] = re.sub(pattern, "DIGITO",aux[0])
  aux[0]= ''.join(ch for ch in aux[0] if ch not in exclude)
  if len(aux)>1 and aux[1][0]!= "O":
    if aux[1][0] =="B":
      if  len(aux_list) !=0:
        named_entity.append(aux[1][2:])
        entity.append(aux_list)
        aux_list = []
        aux_list.append(aux[0])
      else:  
        aux_list.append(aux[0])
    elif aux[1][0] =="I":
        aux_list.append(aux[0])

f = open("entities.txt", "w")
for i in xrange(len(entity)):
  for j in xrange(len(entity[i])):
      f.write("{} {}\t".format(entity[i][j]))
  #f.write("{}\t {}\n".format(entity[i], named_entity[i]))

        

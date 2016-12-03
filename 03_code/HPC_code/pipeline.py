import unicodedata
import pandas as pd
import os
import io
import re
import string
import gensim
import numpy as np
from tempfile import TemporaryFile
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine
from sklearn import cluster
import pickle

#/home/mc3784/OPTIMIZATION/NER_Spectral/03_code/
train_path = "/Volumes/limoncito/NLP/NER_Spectral/01_raw_data/train.txt"
eval_path = "/Volumes/limoncito/NLP/NER_Spectral/01_raw_data/validation.txt"
model_path = '/Volumes/limoncito/NLP/Words_embedding/SBW-vectors-300-min5.bin'

def replace_digit(item):
    pattern = 'DIGITO\sDIGITO'
    for i in range(10):
      item = re.sub(pattern, "DIGITO ",item)
    pattern = 'DIGITO[\.\,\-]DIGITO'
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



entity = []
named_entity = []

exclude = set(string.punctuation)
pattern ='[0-9]+'
aux_list=[]
for line in lines:
  aux=line.strip().split(" ")
  aux[0] = re.sub(pattern, "DIGITO",aux[0])
  aux_string=replace_digit(aux[0])
  if len(aux)>1 and aux[1][0]!= "O":
    if aux[1][0] =="B":
      if  len(aux_list) !=0 and aux_string!="":
        named_entity.append(aux[1][2:])
        entity.append(aux_list)
        aux_list = []
        aux_list.append(aux_string)
      else:  
        aux_list.append(aux_string)
    elif aux[1][0] =="I":
      aux_list.append(aux_string)

model = gensim.models.Word2Vec.load(model_path)


i = 0
named_entity_f= []
entity_embedding = []

for element in entity:
  dimension_ent = len(entity)
  avg_ent = []
  for item in element:
    try:
      avg_ent.append(model[item])
    except:
      pass
  if avg_ent != []:    
    avg_ent = np.array(avg_ent)
    avg_ent = np.mean(avg_ent, axis = 0)
    entity_embedding.append(avg_ent)
    named_entity_f.append(named_entity[i])
  i +=1

print(len(entity))
print(len(named_entity))


entity_embedding =np.array(entity_embedding)

#Spectral CLustering 
pickle.dump(named_entity_f, open("true_labels.p", "wb"))
print("starting spectral")
spectral = cluster.SpectralClustering(n_clusters=10, eigen_solver='arpack', n_init=1)#, affinity="nearest_neighbors"
spectral.fit(entity_embedding)
print spectral.labels_

pickle.dump(spectral.labels_, open("predicted_labels.p", "wb"))
#labels = pickle.load(open("labels.p", "rb"))


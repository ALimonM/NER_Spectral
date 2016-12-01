import unicodedata
import pandas as pd
import os
import io
import re
import string
import gensim
import numpy as np
from tempfile import TemporaryFile

from sklearn import cluster
import pickle


#os.chdir('/Volumes/limoncito/NLP/NER_Spectral/')

train=io.open("/home/mc3784/OPTIMIZATION/NER_Spectral/03_code/train.txt",'r', encoding = 'utf-8')
evaluation = io.open("/home/mc3784/OPTIMIZATION/NER_Spectral/03_code/validation.txt",'r', encoding = 'utf-8')

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


model = gensim.models.Word2Vec.load('/scratch/mc3784/OPT/run-9250165/skip_5')

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

entity_embedding =np.array(entity_embedding)
print(entity_embedding.shape)
#print(named_entity_f)

pickle.dump(named_entity_f, open("true_labels.p", "wb"))
print("starting spectral")
spectral = cluster.SpectralClustering(n_clusters=10, eigen_solver='arpack', n_init=1)#, affinity="nearest_neighbors"
spectral.fit(entity_embedding)
print spectral.labels_

pickle.dump(spectral.labels_, open("predicted_labels.p", "wb"))
#labels = pickle.load(open("labels.p", "rb"))
#print labels
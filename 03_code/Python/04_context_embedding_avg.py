import gensim
import unicodedata
import pandas as pd
import sys
import csv
import os
import io
import string
import re
from sys import exit
import codecs
from sklearn import cluster
import pickle
import numpy as np

#Convert train and text 


context_words = 2
model_path = '/Volumes/limoncito/NLP/Words_embedding/SBW-vectors-300-min5.bin'
context_prep_path = "/Volumes/limoncito/NLP/NER_Spectral/02_clean_data/context_prep.txt"
output_path = "/Volumes/limoncito/NLP/NER_Spectral/02_clean_data/context_entity.txt"
output_path_2 = "/Volumes/limoncito/NLP/NER_Spectral/02_clean_data/context_named_entity.txt"



context_prep=io.open(context_prep_path,'r', encoding = 'utf-8')

lines = []
for line in context_prep:
   line = re.sub(' +',' ',line)
   line = line.replace(" \n", "")
   lines.append(line.strip("\n").strip())

context_name_ent = []
named_entity = []
for item in lines:
    list_entity = re.findall(r'XXXAA(.*?)XXXAA',item)
    n = len(list_entity)
    if n != 0:
       for element in list_entity:
           named_entity.append(element)
           p = len(named_entity)
           item = item.replace(element, element[3:])
           item_list = item.split("XXXAA", 2)
       while len(item_list) > 1 :
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
    m = len(context_name_ent)
    if m!=p:
       print(item)
       break
      
print(len(context_name_ent))
print(len(named_entity))



######## Word2Vector
#model = gensim.models.Word2Vec.load(model_path)
model = gensim.models.Word2Vec.load_word2vec_format(model_path, binary=True)

thefile = open(output_path, 'w')

i = 0
named_entity_f = []
entity_embedding = []
for element in context_name_ent:
   avg_ent = []
   list_avg = element + named_entity[i][3:].split(" ")
   for item in list_avg:
      try:
         avg_ent.append(model[item])
      except:
         pass
   if avg_ent != []:
      avg_ent = np.array(avg_ent)
      avg_ent = np.mean(avg_ent, axis = 0)
      entity_embedding.append(avg_ent)
      for element in list_avg:
         thefile.write("%s\t" % element.encode('utf-8'))
      thefile.write("%s\n" % named_entity[i][:3].encode('utf-8')) 
   i +=1

entity_embedding =np.array(entity_embedding)
print(len(named_entity_f))
#Spectral CLustering 
pickle.dump(named_entity_f, open("true_labels.p", "wb"))
print("starting spectral")
spectral = cluster.SpectralClustering(n_clusters=10, eigen_solver='arpack', n_init=1)#, affinity="nearest_neighbors"
spectral.fit(entity_embedding)
print spectral.labels_

pickle.dump(spectral.labels_, open("predicted_labels.p", "wb"))
#labels = pickle.load(open("labels.p", "rb"))



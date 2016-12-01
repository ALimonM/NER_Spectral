import gensim
import nltk
import unicodedata
import pandas as pd
import os
import io
#nltk.download()

os.chdir('/Volumes/Seagate Backup Plus Drive/NLP/NER_Spectral/04_word_embedding/')


read_file=io.open("train.txt",'r', encoding = 'utf-8')
entity = []
named_entity = []
p = 0
for line in read_file:
  aux=line.strip().split(" ")
  if len(aux)>1 and aux[1]!="O":
    entity.append(aux[0].replace(".", ""))
    named_entity.append(aux[1].replace(".", ""))


fname = "vocab.txt"
read_file=io.open("vocab.txt",'r', encoding = 'utf-8')
vocab= [line.strip() for line in read_file]

for element in entity:
    if element in vocab:
        a = 1
        #print(element)
    else:
        print(element)


intersection=list(set(vocab) & set(entity))
print(intersection[1:100])



#load matrix
#model = gensim.models.Word2Vec.load_word2vec_format('SBW-vectors-300-min5.bin', binary=True)
#model = gensim.models.Word2Vec.load('skip_5')
#print(model['Museo'])

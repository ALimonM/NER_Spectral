import gensim
import unicodedata
import pandas as pd
import sys
import csv
import os

os.chdir('/Volumes/Seagate Backup Plus Drive 1/NLP/NER_Spectral/02_clean_data/Word_embedding_Default/')  
model = gensim.models.Word2Vec.load_word2vec_format('SBW-vectors-300-min5.bin', binary=True)

thefile = open('vocab.txt', 'w')
print(model.vocab.keys()[1:3000])

for item in model.vocab.keys():
  thefile.write("%s\n" % item.encode('utf8'))

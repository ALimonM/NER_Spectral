import unicodedata
import pandas as pd
import os
import io
import re
import string
import gensim
import nltk


os.chdir('/Volumes/Seagate Backup Plus Drive/NLP/NER_Spectral/')

train=io.open("02_clean_data/entities.txt",'r', encoding = 'utf-8')
vocab = io.open('02_clean_data/Word_embedding_Default/vocab.txt','r', encoding = 'utf-8')

entity = []
for line in train:
  entity.append(line.split(" ")[0])
  print(line)



import gensim
import nltk
import unicodedata
import pandas as pd
import os
#nltk.download()

os.chdir('/Volumes/Seagate Backup Plus Drive/NLP/NER_Spectral/02_clean_data/')

#load matrix
model = gensim.models.Word2Vec.load_word2vec_format('SBW-vectors-300-min5.bin', binary=True)
#model = gensim.models.Word2Vec.load('skip_5')
print(model['oov'])

import os
from os import listdir
from os.path import isfile, join
import re

os.chdir('/Volumes/Seagate Backup Plus Drive/NLP/Words_embedding/clean_corpus/')


mypath = 'spanish_billion_words/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

lines = []
for file in onlyfiles:
  read_file=open('spanish_billion_words/'+ file,'r')
  thefile = open('spanish_billion_words_processed/'+ file + '.txt', 'w')
  for line in read_file:
    for i in range(20):
      pattern = 'DIGITO DIGITO'
      if re.findall(pattern,line):
        line= re.sub(pattern, "DIGITO",line)
    thefile.write("%s" % line)
  
  

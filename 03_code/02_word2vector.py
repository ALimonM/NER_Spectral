#Final script
import gensim, logging
import os

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            print(fname)
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

sentences = MySentences('/Volumes/Seagate Backup Plus Drive/NLP/Words_embedding/clean_corpus/spanish_billion_words/') 
model = gensim.models.Word2Vec(sentences,min_count=5, sg = 1, size=200,
                               window=5,negative = 5, workers=4)

model.save('skip_5')

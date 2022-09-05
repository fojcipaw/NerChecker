'''
Created on 5 wrz 2022

@author: fojcjpaw
'''
from ner.ner_lib import Ner_lib
import nltk

class Nltk_lib(Ner_lib):
    def __init__(self, lib_map):
        super().__init__("nltk", nltk.__version__, lib_map)
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
    
    def init_language(self, language_name):
        pass

    def prepare(self, doc):
        '''
        prepare dictionary of entities
        ents={entity1:[label1, label2, etc],
              entity2:[label1, label2, etc],}
        '''
        nltk_doc = []
        for chunk in doc:
            if hasattr(chunk, 'label'):
                nltk_doc.append(chunk)
      
        ents = {}
        for doc_element in nltk_doc:
            entity = ' '.join(c[0] for c in doc_element)
            label = doc_element.label()
            if entity in ents:
                ents[entity].append(label)
            else:
                ents[entity] = [label]
        return ents
    
    def process(self, text):
        tokens = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(tokens)
        doc = nltk.chunk.ne_chunk(tagged)
        return doc
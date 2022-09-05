'''
Created on 5 wrz 2022

@author: fojcjpaw
'''
from ner.ner_lib import Ner_lib
import spacy

class Spacy_lib(Ner_lib):
    def __init__(self, lib_map):
        super().__init__("spacy", spacy.__version__, lib_map)
        self.nlp = spacy.load("en_core_web_sm")
    
    def prepare(self, doc):
        '''
        prepare dictionary of entities
        ents={entity1:[label1, label2, etc],
              entity2:[label1, label2, etc],}
        '''
        ents = {}
        for ent in doc.ents:
            entity = ent.text
            label = ent.label_
            if entity in ents:
                ents[entity].append(label)
            else:
                ents[entity] = [label]
        return ents
    
    def process(self, text):
        doc = self.nlp(text)
        return doc
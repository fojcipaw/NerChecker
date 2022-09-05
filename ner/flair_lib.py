'''
Created on 5 wrz 2022

@author: fojcjpaw
'''
from ner.ner_lib import Ner_lib
from flair.data import Sentence
from flair.models import SequenceTagger
import flair

class Flair_lib(Ner_lib):
    def __init__(self, lib_map):
        super().__init__("flair", flair.__version__, lib_map)
        self.tagger = SequenceTagger.load('ner')
    
    def prepare(self, doc):
        '''
        prepare dictionary of entities
        ents={entity1:[label1, label2, etc],
              entity2:[label1, label2, etc],}
        '''
        ents = {}
        for doc_element in doc.get_spans('ner'):
            entity = doc_element.text
            label = doc_element.get_label().value
            if entity in ents:
                ents[entity].append(label)
            else:
                ents[entity] = [label]
                
        return ents
    
    def process(self, text):
        doc = Sentence(text)
        self.tagger.predict(doc)
        return doc
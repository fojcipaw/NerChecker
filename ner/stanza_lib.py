'''
Created on 5 wrz 2022

@author: fojcjpaw
'''
from ner.ner_lib import Ner_lib
import stanza

class Stanza_lib(Ner_lib):
    def __init__(self, lib_map):
        super().__init__("stanza", stanza.__version__, lib_map)

    def init_language(self, language_name):
        if language_name == "english":
            stanza.download('en') # download English model
            self.nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')
        elif language_name == "germany":
            stanza.download('de') # download German model
            self.nlp = stanza.Pipeline(lang='de', processors='tokenize,ner') # initialize German neural pipeline
        else:
            raise Exception("Unsupported language")

    def prepare(self, doc):
        '''
        prepare dictionary of entities
        ents={entity1:[label1, label2, etc],
              entity2:[label1, label2, etc],}
        '''
        ents = {}
        for ent in doc.ents:
            entity = ent.text
            label = ent.type
            if entity in ents:
                ents[entity].append(label)
            else:
                ents[entity] = [label]
        return ents
    
    def process(self, text):
        doc = self.nlp(text)
        return doc
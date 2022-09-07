'''
Created on 5 wrz 2022

@author: fojcjpaw
'''
from ner.ner_lib import Ner_lib
from trankit import Pipeline
import trankit

class Trankit_lib(Ner_lib):
    def __init__(self, lib_map):
        super().__init__("trankit", trankit.__version__, lib_map)
    
    def init_language(self, language_name):
        if language_name == "english":
            self.p = Pipeline('english')
        elif language_name == "german":
            p = Pipeline('german')
        else:
            raise Exception("Unsupported language")

    def prepare(self, doc):
        '''
        prepare dictionary of entities
        ents={entity1:[label1, label2, etc],
              entity2:[label1, label2, etc],}
        '''
        trankit_doc = []
        for sentence in doc['sentences']:
            tokens = sentence['tokens']
            lemma = ""
            for t in tokens:
                lemma_part = t['text']
                label = t['ner']
            
                if label[0:2] == "B-":
                    lemma = lemma_part
                elif label[0:2] == "I-":
                    lemma += " " + lemma_part
                elif label[0:2] == "E-": #?
                    lemma += " " + lemma_part
                    trankit_doc.append((lemma,label[2:]))
                else:
                    pass
        
        ents = {}
        for doc_element in trankit_doc:
            entity = doc_element[0]
            label = doc_element[1]
            if entity in ents:
                ents[entity].append(label)
            else:
                ents[entity] = [label]
                
        return ents
    
    def process(self, text):
        doc = self.p.ner(text)
        return doc
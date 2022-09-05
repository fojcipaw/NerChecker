'''
Created on 31 sie 2022

@author: fojcjpaw
'''
import time
import pandas as pd
from files_reader.conllu_reader import ConlluReader
from tools.comparators import NerCompare
from tools.results import NerResult
from ner.ner_get import get_lib

class NerChecker:
    def __init__(self, file_path, sentences_limit):
        self.reader = ConlluReader(file_path, sentences_limit)
        self.comparator = NerCompare()
        self.result = NerResult()
        self.df_data = {}
    
    def get_text(self):
        return self.reader.get_text()
    
    def add(self, lib_obj):
        lib_ent, elapsed_time = self.__prepare(lib_obj)
        data = self.comparator.compare(lib_ent, self.reader.get_ents(), lib_obj.get_map())
        data['elapsed_time'] = elapsed_time
        
        data = self.result.get_result(data)
        
        self.df_data.update({lib_obj.get_name(): 
                   [lib_obj.get_version(),
                   data['true_positive_rate'],
                   data['false_positive_rate'],
                   data['positive_predictive_value'],
                   data['f_score'],
                   data['g_score'],
                   data['accuracy'],
                   data['entities lib'],
                   data['entities oryg'],
                   data['elapsed_time'],]
                   })
        
    def __prepare(self, lib_obj):
        st = time.time()
        doc = lib_obj.process(self.get_text())
        et = time.time()
        elapsed_time = et - st
        '''
        prepare dictionary of entities
        ents={entity1:[label1, label2, etc],
              entity2:[label1, label2, etc],}
        '''
        ents = lib_obj.prepare(doc)
        return ents, elapsed_time

    def get_result(self):
        df = pd.DataFrame(self.df_data)
        df.index=['version',
                  'true_positive_rate (recall, sensitivity)',
                  'false_positive_rate (specificity)', 
                  'positive_predictive_value (precision)',
                  'f_score','g_score',
                  'accuracy',
                  'entities lib',
                  'entities oryg',
                  'elapsed time']
        return df
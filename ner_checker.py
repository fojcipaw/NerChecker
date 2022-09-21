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
    def __init__(self, file_path, language, sentences_limit):
        self.reader = ConlluReader(file_path, sentences_limit)
        self.comparator = NerCompare()
        self.result = NerResult()
        self.compare_data = {}
        self.df_data = {}
        self.language = language
        self.lib_ents = {}
    
    def get_text(self):
        return self.reader.get_text()
    
    def add(self, lib_obj):
        lib_obj.init_language(self.language)
        lib_ent, elapsed_time = self.__prepare(lib_obj)
        self.lib_ents.update({lib_obj.get_name():lib_ent})
        compare_data = self.comparator.compare(lib_ent, self.reader.get_ents(), lib_obj.get_map())
        compare_data['elapsed_time'] = elapsed_time
        self.compare_data.update({lib_obj.get_name():compare_data})
        
        data = self.result.get_result(compare_data)
        self.df_data.update(self.result.get_header(data, lib_obj.get_name(), lib_obj.get_version()))
        
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
                  'entities common',
                  'entities lib',
                  'entities oryg',
                  'elapsed time']
        return df
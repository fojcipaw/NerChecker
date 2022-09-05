'''
Created on 5 wrz 2022

@author: fojcjpaw
'''
class Ner_lib():
    def __init__(self, name, version, lib_map):
        self.name = name
        self.lib_map = lib_map
        self.version = version
    
    def get_map(self):
        return self.lib_map

    def get_name(self):
        return self.name
    
    def get_version(self):
        return self.version

    def prepare(self, doc):
        '''
        prepare dictionary of entities
        ents={entity1:[label1, label2, etc],
              entity2:[label1, label2, etc],}
        '''
        return None

    def process(self, text):
        return None
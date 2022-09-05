'''
Created on 5 wrz 2022

@author: fojcjpaw
'''
from ner.spacy_lib import Spacy_lib
from ner.stanza_lib import Stanza_lib
from ner.trankit_lib import Trankit_lib
from ner.nltk_lib import Nltk_lib

def get_lib(lib_name, lib_map):
    if lib_name == "spacy":
        return Spacy_lib(lib_map)
    elif lib_name == "stanza":
        return Stanza_lib(lib_map)
    elif lib_name == "trankit":
        return Trankit_lib(lib_map)
    elif lib_name == "nltk":
        return Nltk_lib(lib_map)
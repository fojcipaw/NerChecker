'''
Created on 24 sie 2022

@author: fojcjpaw
'''
from conllu import parse
class ConlluReader:
    class Ents:
        def __init__(self):
            self.ents = {}
            self.one_sentence_with_ents = []
            self.sentences_with_ents=[]
        
        def add(self, entity, label):
            self.one_sentence_with_ents.append((entity, label))
            if entity in self.ents:
                self.ents[entity].append(label)
            else:
                self.ents[entity] = [label]
        
        def add_sentence(self, sentence):
            self.sentences_with_ents.append((sentence, self.__get_one_sentence_with_ents()))
            self.one_sentence_with_ents = []
        
        def get_sentences_with_ents(self):
            return self.sentences_with_ents
    
        def get_ents(self):
            return self.ents
        
        def __get_one_sentence_with_ents(self):
            return self.one_sentence_with_ents
        
    def __init__(self, path_to_file):
        sentences = self.__conllu_prepare_sentences(path_to_file)
        self.sent_and_ents, self.ents, self.text = self.__prepare_doc_and_text(sentences)
    
    def get_text(self):
        return self.text
    
    def get_sent_and_ents(self):
        return self.sent_and_ents

    def get_ents(self):
        return self.ents

    def __conllu_prepare_sentences(self, path_to_file):
        with open(path_to_file) as f:
            annotations = f.read()
        sentences = parse(annotations)
        return sentences

    def __prepare_doc_and_text(self, sentences, sentences_limit = 0):
        """
        sent_and_ents - list of sentences with ents, 
            eg. [('In January 2003 he moved to Sartid Smederevo .', [('Sartid', 'LOC'), ('Smederevo', 'LOC')]),
                [<sentence>, [(ent, label), (ent, label)]]
        """
        text_list=[]
        if sentences_limit == 0:
            sentences_limit = len(sentences)
        ents=ConlluReader.Ents()

        for sentence in sentences[:sentences_limit]:
            sent=[] #whole sentence
            form_list=[] #whole entity
            lemma_saved = ""
            for token in sentence:
                #id = token['id']
                lemma = token['lemma'] #label
                form = token['form']
                text_list.append(form)
                sent.append(form)
                
                if lemma[0:2] == "B-":
                    if form_list:
                        ents.add(" ".join(form_list),lemma_saved) #there are cases where is only B- without I-
                    form_list = [form]
                    lemma_saved = lemma[2:]
                elif lemma[0:2] == "I-":
                    form_list.append(form)
                elif lemma[0:2] == "E-": #?
                    form_list.append(form) #?
                else:
                    if form_list:
                        ents.add(" ".join(form_list),lemma_saved)
                    form_list = []
                    lemma_saved = ""
            ents.add_sentence(" ".join(sent))
            
        return ents.get_sentences_with_ents(), ents.get_ents(), " ".join(text_list)
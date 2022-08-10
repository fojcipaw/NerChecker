from conllu import parse
import pandas as pd
import time

class NerChecker:
  def __init__(self, path_to_file, sentences_limit=0, file_type="conllu"):
    if file_type=="conllu":
        sentences = self.__conllu_prepare_sentences(path_to_file)
        self.__conllu_prepare_text(sentences, sentences_limit)
    else:
        pass
    self.data = {}
  
  def __nlp(self, nlp_action):
    st = time.time()
    doc = nlp_action(self.get_text())
    et = time.time()
    elapsed_time = et - st
    return elapsed_time, doc

  def add(self, lib_name, version, nlp_action, label_mapping):
    elapsed_time, doc = self.__nlp(nlp_action)
    self.__compare(lib_name, version, elapsed_time, doc, label_mapping)
  
  def get_df(self, lib_name):
    oryg_entities = []
    oryg_labels = []
    lib_entities = []
    lib_labels = []
    estimates = []
    for d in self.data[lib_name]["data"]:
        oryg_entities.append(d[0])
        oryg_labels.append(d[1])
        lib_entities.append(d[2])
        lib_labels.append(d[3])
        estimates.append(d[4])
        
        df = pd.DataFrame({'oryg entity':oryg_entities,'oryg label':oryg_labels,lib_name+' entity':lib_entities, lib_name+' label':lib_labels, 'estimates':estimates})
    return df

  def get_text(self):
    return self.text
    
  def get_results(self):
    import math
    
    data={}
    for lib_name, value in self.data.items():
        qmc = value["qmc"]
        lib_elapsed_time = value["elapsed_time"]
        version = value["version"]
        #print(qmc)
        #	(sensitivity, recall) true positive rate = TP/(TP+FN) = 1 − false negative rate
        recall = "div/0"
        if (qmc['True Positive']+qmc['False Negative']) > 0:
            recall = true_positive_rate=qmc['True Positive']/(qmc['True Positive']+qmc['False Negative'])
        #print("sensitivity = recall = true_positive_rate",true_positive_rate)
        #	(specificity) false positive rate = FP/(FP+TN)
        false_positive_rate = "div/0"
        if (qmc['False Positive']+qmc['True Negative']) > 0:
            false_positive_rate=qmc['False Positive']/(qmc['False Positive']+qmc['True Negative'])
        #print("specificity = false_positive_rate",false_positive_rate)
        # (precision) positive predictive value = TP/(TP+FP)
        precision  = "div/0"
        if (qmc['True Positive']+qmc['False Positive']) > 0:
            precision = positive_predictive_value = qmc['True Positive']/(qmc['True Positive']+qmc['False Positive'])
        #print("precision = positive_predictive_value",positive_predictive_value)
        #F-score is the harmonic mean of precision and recall
        f_score = "div/0"
        if (precision+recall)) > 0:
            f_score = 2 * ((precision*recall)/(precision+recall))
        #print("F-score",f_score)
        #G-score is the geometric mean of precision and recall
        g_score = math.sqrt(precision*recall)
        #print("G-score",g_score)
        #Accuracy
        accuracy=(qmc['True Positive']+qmc['True Negative'])/(qmc['True Positive']+qmc['False Positive']+qmc['True Negative']+qmc['False Negative'])
        data.update({lib_name:[version, true_positive_rate,false_positive_rate,positive_predictive_value,f_score,g_score,accuracy, lib_elapsed_time]})

    df = pd.DataFrame(data)
    df.index=["version","true_positive_rate (recall, sensitivity)","false_positive_rate (specificity)", "positive_predictive_value (precision)","f_score","g_score","accuracy","elapsed time"]
    return df
  
  def __compare(self, lib_name, version, elapsed_time, doc, label_mapping):
    """
    function to prepare comparison
    lib_name: name of the nlp library, eg "spacy", "stanza"
    doc : nlp object
    label_mapping : dict (mapping between oryginal label and nlp label, eg {"PER":"PERSON"})
    """
    data = []
    qmc={"True Positive":0,"True Negative":0,"False Positive":0,"False Negative":0} #quality measurement counter
    base_idx = 0

    for o in self.oryg:
        o_entity = o[0]
        o_label = o[1]
        is_added = False

        spans = self.__get_spans(lib_name, doc)

        for idx in range(base_idx, len(spans)):
            l_entity = self.__get_entity(lib_name, spans[idx]) #spans[idx].text
            l_label = self.__get_label(lib_name, spans[idx])
            if self.__is_entity_eq(o_entity, l_entity):

                for j in range(base_idx+1,idx):
                    lj_entity = self.__get_entity(lib_name, spans[j]) #spans[j].text
                    lj_label = self.__get_label(lib_name, spans[j])
                    data.append((None,None,lj_entity,lj_label,"True Negative"))
                    qmc["True Negative"]+=1

                if self.__is_label_eq(o_label, l_label,label_mapping):
                    data.append((o_entity,o_label,l_entity,l_label,"True Positive"))
                    qmc["True Positive"]+=1

                else:
                    data.append((o_entity,o_label,l_entity,l_label,"False Positive"))
                    qmc["False Positive"]+=1

                base_idx = idx+1
                is_added = True
                break

            else:
                pass

        if is_added == False:
            data.append((o_entity,o_label,None,None,"False Negative"))
            qmc["False Negative"]+=1
    self.data.update({lib_name:{"data":data, "qmc":qmc, "elapsed_time":elapsed_time, "version":version}})

  def __conllu_prepare_sentences(self, path_to_file):
    annotations = None
    with open(path_to_file) as f:
        annotations = f.read()
    #parse annotations, get sentences
    sentences = parse(annotations)
    return sentences
  
  def __conllu_prepare_text(self, sentences, sentences_limit):
    self.oryg=[]
    form_list=[]
    text_list=[]
    if sentences_limit == 0:
        sentences_limit = len(sentences)
    for sentence in sentences[:sentences_limit]:
      for token in sentence:
        id = token['id']
        lemma = token['lemma']
        form = token['form']
        text_list.append(form)

        if lemma[0:2] == "B-":
          if form_list:
            self.oryg.append(("_".join(form_list),lemma_saved))
          form_list = [form]
          lemma_saved = lemma[2:]
        elif lemma[0:2] == "I-":
          form_list.append(form)
        elif lemma[0:2] == "E-": #?
          form_list.append(form) #?
        else:
          if form_list:
            self.oryg.append((" ".join(form_list),lemma_saved))
          form_list = []
          lemma_saved = ""
    self.text = " ".join(text_list)

  def __is_entity_eq(self, value_first, value_second):
    if value_first == value_second:
        return True
    elif value_first == "the "+value_second:
        return True
    elif value_first == "The "+value_second:
        return True
    elif "the "+value_first == value_second:
        return True
    elif "The "+value_first == value_second:
        return True
    else:
        return False
  
  def __is_label_eq(self, o_label, l_label, label_mapping):
    if o_label == l_label:
        return True
    
    if o_label in label_mapping and label_mapping[o_label] == l_label:
      return True
    
    if l_label in label_mapping and label_mapping[l_label] == o_label:
      return True
    
    return False
  
  def __get_spans(self, lib_name, doc):
    if lib_name == "flair":
      return doc.get_spans('ner')
    if lib_name == "nltk":
      ents = []
      for chunk in doc:
        if hasattr(chunk, 'label'):
          ents.append(chunk)
      return ents
    elif lib_name == "trankit":
      return self.__prepare_trankit_doc(doc)
    else:
      return doc.ents

  def __get_entity(self, lib_name, entity):
    print(lib_name, entity) #TODO
    if lib_name == "nltk":
      return ' '.join(c[0] for c in entity)
    elif lib_name == "trankit":
      return entity[0]
    else:
      return entity.text

  def __get_label(self, lib_name, entity):
    if lib_name == "spacy":    
      return entity.label_
    elif lib_name == "stanza":    
      return entity.type
    elif lib_name == "flair":
      return entity.get_label().value
    elif lib_name == "nltk":
      return entity.label()
    elif lib_name == "trankit":
      return entity[1]
    else:      
      return None #Error
  
  def __prepare_trankit_doc(self, doc):
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
    return trankit_doc
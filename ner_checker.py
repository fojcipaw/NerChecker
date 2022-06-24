from conllu import parse
import pandas as pd
import time

class NerChecker:
  def __init__(self, path_to_file, file_type="conllu", sentences_limit=0):
    if file_type=="conllu":
        sentences = self.__conllu_prepare_sentences(path_to_file)
        self.__conllu_prepare_text(sentences, sentences_limit)
    else:
        pass
    self.data = {}
  
  def nlp(self, nlp):
    st = time.time()
    doc = nlp(self.get_text())
    et = time.time()
    elapsed_time = et - st
    return doc, elapsed_time
  
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
        #print(qmc)
        #	(sensitivity, recall) true positive rate = TP/(TP+FN) = 1 − false negative rate
        recall = true_positive_rate=qmc['True Positive']/(qmc['True Positive']+qmc['False Negative'])
        #print("sensitivity = recall = true_positive_rate",true_positive_rate)
        #	(specificity) false positive rate = FP/(FP+TN) 
        false_positive_rate=qmc['False Positive']/(qmc['False Positive']+qmc['True Negative'])
        #print("specificity = false_positive_rate",false_positive_rate)
        # (precision) positive predictive value = TP/(TP+FP)
        precision = positive_predictive_value = qmc['True Positive']/(qmc['True Positive']+qmc['False Positive'])
        #print("precision = positive_predictive_value",positive_predictive_value)
        #F-score is the harmonic mean of precision and recall
        f_score = 2*math.sqrt((precision*recall)/(precision+recall))
        #print("F-score",f_score)
        #G-score is the geometric mean of precision and recall
        g_score = math.sqrt(precision*recall)
        #print("G-score",g_score)
        #Accuracy
        accuracy=(qmc['True Positive']+qmc['True Negative'])/(qmc['True Positive']+qmc['False Positive']+qmc['True Negative']+qmc['False Negative'])
        data.update({lib_name:[true_positive_rate,false_positive_rate,positive_predictive_value,f_score,g_score,accuracy, lib_elapsed_time]})

    df = pd.DataFrame(data)
    df.index=["true_positive_rate (recall, sensitivity)","false_positive_rate (specificity)", "positive_predictive_value (precision)","f_score","g_score","accuracy","elapsed time"]
    return df

  def compare(self, lib_name, elapsed_time, doc, label_mapping):
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

        for idx in range(base_idx,len(doc.ents)):
            l_entity = doc.ents[idx].text
            l_label = self.__get_label(doc.ents[idx])
            if self.__is_entity_eq(o_entity, l_entity):

                for j in range(base_idx+1,idx):
                    lj_entity = doc.ents[j].text
                    lj_label = self.__get_label(doc.ents[j])
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
    self.data.update({lib_name:{"data":data, "qmc":qmc, "elapsed_time": elapsed_time}})

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
  
  def __get_label(self, entity):
    label = ""
    try:
      label = entity.label_
    except:
      label = entity.type
    return label
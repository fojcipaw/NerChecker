from conllu import parse

class NerChecker:
  def __init__(self, path_to_conllu_file):
    #read annotations
    annotations = None
    with open(path_to_conllu_file) as f:
        annotations = f.read()
    #parse annotations, get sentences
    sentences = parse(annotations)

    #prepare:
    # - self.text
    # - self.data
    self.data={}
    form_list=[]
    form_list_all=[]
    for sentence in sentences:
      for token in sentence:
        id = token['id']
        lemma = token['lemma']
        form = token['form']
        form_list_all.append(form)

        if lemma[0:2] == "B-":
          if form_list:
            self.data.update({"_".join(form_list):lemma_saved})
          form_list = [form]
          lemma_saved = lemma[2:]
        elif lemma[0:2] == "I-":
          form_list.append(form)
        else:
          if form_list:
            self.data.update({"_".join(form_list):lemma_saved})
          form_list = []
          lemma_saved = ""
    self.text = " ".join(form_list_all)

    #comparate members
    self.compare_list = []

  def get_text(self):
    return self.text

  def prepare_comparison(self, doc, label_mapping_dict):
    for ent in doc.ents:
      entity = ent.text
      label = ent.label_
      self.__add_entity(entity.replace(" ","_"), label, label_mapping_dict)

  def get_compare_list(self):
    return self.compare_list
  
  def show_statistics(self):
    positive=0
    negative=0
    not_found=0
    for compare_list in self.get_compare_list():
      if compare_list["found"]:
        if compare_list["match"]:
          positive+=1
        else:
          negative+=1
      else:
        not_found+=1
    print({"positive":positive,"negative":negative,"not_found":not_found})
  
  def show_in_array(self):
    import pandas as pd

    oryg_entities = []
    oryg_labels = []
    lib_entities = []
    lib_labels = []
    founds = []
    matches = []

    for compare_list in self.get_compare_list():
      oryg_entities.append(compare_list["oryg_entity"])
      oryg_labels.append(compare_list["oryg_label"])
      lib_entities .append(compare_list["entity"])
      lib_labels.append(compare_list["label"])
      founds.append(compare_list["found"])
      matches.append(compare_list["match"])

    return pd.DataFrame({'oryg_entity':oryg_entities,'oryg_label':oryg_labels,'entity':lib_entities, 'label':lib_labels,'found':founds,'match':matches})

  def __add_entity_to_data(self, oryg_entity, oryg_label, entity, label, label_mapping_dict):
    match = False
    if oryg_label in label:
      match = True
    else:
      if oryg_label in label_mapping_dict:
        mapped_label = label_mapping_dict[oryg_label]
        if mapped_label in label:
          match = True
    if match:
      self.compare_list.append({"entity":entity,"label":label, "oryg_entity":oryg_entity, "oryg_label":oryg_label,"found":True,"match":True})
    else:
      self.compare_list.append({"entity":entity,"label":label, "oryg_entity":oryg_entity, "oryg_label":oryg_label,"found":True,"match":False})

  def __add_entity(self, entity, label, label_mapping_dict):
    for oryg_entity, oryg_label in self.data.items():
      if oryg_entity in entity:
        self.__add_entity_to_data(oryg_entity, oryg_label, entity, label, label_mapping_dict)
        return
      else:
        pass
    self.compare_list.append({"entity":entity,"label":label, "oryg_entity":None, "oryg_label":None,"found":False,"match":False})
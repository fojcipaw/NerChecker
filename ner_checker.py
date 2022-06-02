!pip install conllu
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
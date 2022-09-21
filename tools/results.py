'''
Created on 31 sie 2022

@author: fojcjpaw
'''
import math

class NerResult:
    def __init__(self):
        pass
    
    def get_header(self, data, lib_name, lib_version):
        return {lib_name: 
               [lib_version,
               data['true_positive_rate'],
               data['false_positive_rate'],
               data['positive_predictive_value'],
               data['f_score'],
               data['g_score'],
               data['accuracy'],
               data['entities common'],
               data['entities lib'],
               data['entities oryg'],
               data['elapsed_time'],]
               }
    
    def get_result(self, data):
        #print(data)
        #    (sensitivity, recall) true positive rate = TP/(TP+FN) = 1 − false negative rate
        recall = true_positive_rate = 0
        if (len(data['TP'])+len(data['FN'])) > 0:
            recall = true_positive_rate = len(data['TP'])/(len(data['TP'])+len(data['FN']))
        #print("sensitivity = recall = true_positive_rate",true_positive_rate)
        #    (specificity) false positive rate = FP/(FP+TN)
        false_positive_rate = 0
        if (len(data['FP'])+len(data['TN'])) > 0:
            false_positive_rate=len(data['FP'])/(len(data['FP'])+len(data['TN']))
        #print("specificity = false_positive_rate",false_positive_rate)
        # (precision) positive predictive value = TP/(TP+FP)
        precision  = positive_predictive_value = 0
        if (len(data['TP'])+len(data['FP'])) > 0:
            precision = positive_predictive_value = len(data['TP'])/(len(data['TP'])+len(data['FP']))
        #print("precision = positive_predictive_value",positive_predictive_value)
        #F-score is the harmonic mean of precision and recall
        f_score = 0
        if (precision+recall) > 0:
            f_score = 2 * ((precision*recall)/(precision+recall))
        #print("F-score",f_score)
        #G-score is the geometric mean of precision and recall
        g_score = math.sqrt(precision*recall)
        #print("G-score",g_score)
        #Accuracy
        accuracy=(len(data['TP'])+len(data['TN']))/(len(data['TP'])+len(data['FP'])+len(data['TN'])+len(data['FN']))
        
        l1 = list(d[0] for d in data['TP'])
        l2 = list(d[0] for d in data['FP'])
        entities_common = len(set(l1+l2))
        
        return {'true_positive_rate':true_positive_rate,
                'false_positive_rate':false_positive_rate,
                'positive_predictive_value':positive_predictive_value,
                'f_score':f_score,
                'g_score':g_score,
                'accuracy':accuracy,
                'entities common': entities_common,
                'entities lib':data['len__lib_ent'],
                'entities oryg':data['len__oryg_ent'],
                'elapsed_time': data['elapsed_time']
                }
'''
Created on 31 sie 2022

@author: fojcjpaw
'''
from tools.results import NerResult
class NerCompare:
    def __init__(self):
        pass
    
    def compare(self, lib_ent, oryg_ent, label_map):
        data = {"TP":[],
            "TN":[],
            "FP":[],
            "FN":[],}
        '''
        comparison - build list lib_*
        - search for ent items and build:
            lib_entity_found_in_both, 
            lib_entity_found_in_one
        '''
        lib_entity_found_in_both = []
        lib_entity_found_in_one = []
        for entity, label in lib_ent.items():
            if entity in oryg_ent:
                lib_entity_found_in_both.append((entity,oryg_ent[entity]))
            else:
                lib_entity_found_in_one.append((entity, label))
        
        '''
        comparison - build list oryg_*
        - search for oryg ent items and build:
            oryg_entity_found_in_both, 
            oryg_entity_found_in_one
        '''
        oryg_entity_found_in_both = []
        oryg_entity_found_in_one = []
        for oryg_entity, oryg_label in oryg_ent.items():
            if oryg_entity in lib_ent:
                oryg_entity_found_in_both.append((oryg_entity,lib_ent[oryg_entity]))
            else:
                oryg_entity_found_in_one.append((oryg_entity, oryg_label))
            
    
        data["len__oryg_ent"] = len(oryg_ent)
        data["len__lib_ent"] = len(lib_ent)
        '''
        comparison - found in both 
        '''
        if len(lib_entity_found_in_both) != len(oryg_entity_found_in_both):
            print("ERROR entity")
            exit(1)
            
        for i in range (0, len(lib_entity_found_in_both)):
            labels_lib = lib_entity_found_in_both[i][1]
            labels_oryg = oryg_entity_found_in_both[i][1]
            
            size_lib = len(labels_lib)
            size_oryg = len(labels_oryg)
            
            size_min = min(size_lib,size_oryg)
            size_max = max(size_lib,size_oryg)
            
            is_less_in_lib = (size_oryg > size_lib)
            
            for j in range (0, size_min):
                if self.__is_label_eq(labels_lib[j], labels_oryg[j], label_map):
                    #print("TRUE POSITIVE: ", lib_entity_found_in_both[i][0], labels_lib[j])
                    data["TP"].append((lib_entity_found_in_both[i][0], labels_lib[j]))
                else:
                    #print("FALSE POSITIVE: ", lib_entity_found_in_both[i][0], labels_lib[j], labels_oryg[j])
                    data["FP"].append((lib_entity_found_in_both[i][0], labels_lib[j], labels_oryg[j]))
            
            for k in range(size_min, size_max):
                if is_less_in_lib:
                    #print("FALSE NEGATIVE: ", lib_entity_found_in_both[k][0], labels_oryg[k])
                    data["FN"].append((lib_entity_found_in_both[k][0], labels_oryg[k]))
                else:
                    #print("TRUE NEGATIVE: ", lib_entity_found_in_both[k][0], labels_lib[k])
                    data["TN"].append((lib_entity_found_in_both[k][0], labels_lib[k]))
        
        '''
        comparison - found only in lib, means: TRUE NEGATIVE 
        '''
        for entity in lib_entity_found_in_one:
            #print("TRUE NEGATIVE: ", entity[0], entity[1])
            data["TN"].append((entity[0], entity[1]))
        
        '''
        comparison - found only in oryg, means: FALSE NEGATIVE 
        '''
        for entity in oryg_entity_found_in_one:
            #print("FALSE NEGATIVE: ", entity[0], entity[1])
            data["FN"].append((entity[0], entity[1]))
        
        return data
    
    def __is_label_eq(self, o_label, l_label, label_mapping):
        if o_label == l_label:
            return True
        
        if o_label in label_mapping and label_mapping[o_label] == l_label:
            return True
        
        if l_label in label_mapping and label_mapping[l_label] == o_label:
            return True
        
        return False
    
if __name__ == "__main__":
    nercompare = NerCompare()
    map = {}
    '''
    ents={entity1:[label1, label2, etc],
          entity2:[label1, label2, etc],}
    '''
    ents_lib = {'a':['1'],
                'b':['1'],
                'd':['1'],
                'e':['1'],
                }
    ents_oryg= {'a':['1'],
                'b':['2'],
                'c':['1'],
                }
    data = nercompare.compare(ents_lib, ents_oryg, map)
    result = NerResult()
    data['elapsed_time'] = 0
    data = result.get_result(data)
    print(data)
from json import loads,dumps
from collections import Counter

def data_remove_duplicates():
    try:
        with open("./sampledata.txt","r") as fobj:
            sample_data = fobj.read()
        sample_data = loads(sample_data)
        print(type(sample_data))
        values_list = [data["id"] for data in sample_data["data"]]
        print("Collecting all unique identifier values :" +str(values_list))
        without_dup = []
        print("Counter of values list "+dumps(Counter(values_list)))
        for id_ in Counter(values_list):
            all_values = [data for data in sample_data["data"] if data['id']==id_]
            print("all_values"+str(all_values))
            without_dup.append(max(all_values, key=lambda x: x['id']))
        print(dumps(without_dup))
    except Exception as e:
        print("Oh! there was an error in your code - "+str(e))
        
        

data_remove_duplicates()
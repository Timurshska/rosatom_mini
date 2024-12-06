import pandas as pd
import json
from json_repair import repair_json
import json_repair
from collections import defaultdict

def find_shallowest_matching_key(json_data, keywords):
    shallowest_key = None
    shallowest_value = None
    shallowest_level = float('inf')

    def recursive_search(obj, current_level):
        nonlocal shallowest_key, shallowest_value, shallowest_level
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key.lower() in keywords:
                    if current_level < shallowest_level:
                        shallowest_key = key
                        shallowest_value = value
                        shallowest_level = current_level
                recursive_search(value, current_level + 1)
        elif isinstance(obj, list):
            for item in obj:
                recursive_search(item, current_level + 1)

    recursive_search(json_data, 0)
    return shallowest_key, shallowest_value


with open(f'result.txt', 'w', encoding='utf-8') as file:
    pass
data = pd.read_csv('data/extracted_items_all (1).csv')['result']
prompt = 'Предмет закупки'
count = len(data)

keywords = ['наименование', 'наименования', 'item', 'items', 'name', 'names', 'itemname',
            'предмет закупки', 'предмет', 'position', 'product', 'equipment', 'тз', 'техническое задание',
            'equipmentname', 'specification']

vals = []
for i in range(count):
    try:
        good_json_string = repair_json(data[i])
        json_data = json.loads(good_json_string)

        if json_data:
            shallowest_key, shallowest_value = find_shallowest_matching_key(json_data, keywords)
            if shallowest_key:
                print(f'{i}: {json_data}')
                with open(f'result.txt', 'a', encoding='utf-8') as file:
                    file.write(f"{json_data}\n")
            else:
                print(f'{i}: No matching keys found')
                print(json_data)
        else:
            continue
    except Exception as e:
        print(f'{i} fail, {e} - error')
        exit()

# prods = []
# for i in vals:
#     if type(i) == list:
#         for j in i:
#             prods.append(j)
#     else:
#         prods.append(i)

# for i in prods:
#     print(i)

# print(len(prods), type(prods))
# print(len(set(prods)))

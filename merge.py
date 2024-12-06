import json
from json_repair import repair_json
import csv

def extract_dictionaries(file_path):
    dictionaries = []
    current_dict = ""

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                if stripped_line.startswith('{') or current_dict:
                    current_dict += stripped_line
                    if stripped_line.endswith('}'):
                        current_dict = repair_json(current_dict)
                        dict_obj = json.loads(current_dict)
                        dictionaries.append(dict_obj)
                        current_dict = ""

    return dictionaries


def preprocess_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            stripped_line = line.strip()
            if stripped_line and stripped_line != '```json' and stripped_line != '```' and stripped_line != '[' and stripped_line != ']':
                outfile.write(line)


input_file = 'merge.txt'
output_file = 'merged.csv'

# Чтение текстового файла
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read().strip()

# Добавляем запятые между словарями
fixed_content = content.replace('}\n{', '},\n{')
dictionaries = json.loads(f'[{fixed_content}]')

# Создание CSV-файла
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Предмет закупки', 'Данные']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for d in dictionaries:
        subject = d.get('Предмет закупки', '')
        data_json = json.dumps(d, ensure_ascii=False)
        row = {'Предмет закупки': subject, 'Данные': data_json}
        writer.writerow(row)

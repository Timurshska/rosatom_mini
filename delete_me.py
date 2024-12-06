import google.generativeai as genai
import os
from PARAMS import key
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from datetime import datetime


def read_first_n_lines(file_path, offset, n):
    lines = ''
    with open(file_path, 'r', encoding='utf-8') as file:
        # Пропускаем первые `offset` строк
        for _ in range(offset):
            if not file.readline():
                break
        # Читаем следующие `n` строк
        for _ in range(n):
            line = file.readline()
            if not line:
                break
            lines += str(line)
    return lines


def count_lines_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return len(lines)


# Пример использования
output_file = 'story1.txt'
input_file = "result.txt"
offset = 1413
step = 15
string_count = count_lines_in_file(input_file)
print(string_count)
with open(output_file, 'w', encoding='utf-8') as file:
    pass
prompt = ("выдели из этих данных все товары для закупки как в формате json, и для каждого из них напиши его характеристики, если они имеются."
          "Если внутри характеристик товара будут списки или словари - убери их. Все ключи должны быть на русском языке. "
          "Для ключа, который соответствует названию объекта используй только одно наименование - 'Предмет закупки' "
          "Никаких комментариев давать не надо.")
os.environ["API_KEY"] = key
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

for _ in range(string_count // step):
    part = read_first_n_lines(input_file, offset, step)
    response = model.generate_content([f"{prompt} \n Данные:{str(part)}"], safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE, }).text
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(f'{response}')
    offset += step

import google.generativeai as genai
import os
from doc_processing import log_func, docx_to_txt
import time
from PARAMS import count_of_file, counter, char_count, key
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from datetime import datetime
import pandas as pd


# Получаем текущие дату и время
date = datetime.now()
date = date.strftime("%Y-%m-%d_%H-%M-%S")
folder_path = 'data/ТЗ(2)'
prompt = ("Укажи перечень товаров на закупку через символ |,"
          " если не можешь найти товар, или текста нет, то пиши только NaN один раз"
          ". Не надо давать никаких комментариев")

if not os.path.exists(f"prompt_experiments/prompt_datas/prompt data {date}"):
    os.makedirs(f"prompt_experiments/prompt_datas/prompt data {date}")

output_file = f'prompt_experiments/prompt_datas/prompt data {date}/prompt_result.txt'

os.environ["API_KEY"] = key
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

input_file = f'prompt_experiments/prompt_datas/prompt data {date}/prompt_input.txt'

txt_file = "test.txt"

with open(
        output_file, 'w'):
    pass
with open(
        input_file, 'w'):
    pass

if not os.path.exists("prompt_experiments/file.txt"):
    excel_file = 'data/размеченный.xlsx'
    df = pd.read_excel(excel_file)
    unique_values = df.iloc[:, 0].unique().tolist()
    with open('prompt_experiments/file.txt', 'w', encoding='utf-8') as file:
        for value in unique_values:
            if not value.endswith('.docx'):
                value = value.strip() + '.docx' # Исправлено: Добавление .docx
            file.write(str(value) + '\n')

with open("prompt_experiments/file.txt", 'r', encoding='utf-8') as file_list:
    filenames = [line for line in file_list]
    filenames = [line[:-1] for line in filenames]
for filename in os.listdir(folder_path):
    if filename.endswith('.docx') and counter < count_of_file and filename in filenames:
        counter += 1
        full_path = os.path.join(folder_path, filename)
        text = docx_to_txt(full_path, txt_file)
        if len(text) > char_count:
            # Делим текст на части по 1 000 000 символов
            parts = [text[i:i + char_count] for i in range(0, len(text), char_count)]
            for part in parts:
                try:
                    response = model.generate_content([f"{prompt} \n Текст:{str(part)}"],
                                                      safety_settings={
                                                          HarmCategory.HARM_CATEGORY_HATE_SPEECH:
                                                              HarmBlockThreshold.BLOCK_NONE,
                                                          HarmCategory.HARM_CATEGORY_HARASSMENT:
                                                              HarmBlockThreshold.BLOCK_NONE,
                                                          HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
                                                              HarmBlockThreshold.BLOCK_NONE,
                                                          HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
                                                              HarmBlockThreshold.BLOCK_NONE, }).text
                    log_func(output_file, input_file, filename, response, part)
                except Exception as e:
                    log_func(output_file, input_file, filename, f"Ошибка при обработке промпта: {e}", part)
                time.sleep(2)  # Задержка в 3 секунды после каждого запроса
        else:
            try:
                response = model.generate_content([f"{prompt} \n Текст:{str(text)}"],
                                                  safety_settings={
                                                      HarmCategory.HARM_CATEGORY_HATE_SPEECH:
                                                          HarmBlockThreshold.BLOCK_NONE,
                                                      HarmCategory.HARM_CATEGORY_HARASSMENT:
                                                          HarmBlockThreshold.BLOCK_NONE,
                                                      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:
                                                          HarmBlockThreshold.BLOCK_NONE,
                                                      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:
                                                          HarmBlockThreshold.BLOCK_NONE, }).text
                log_func(output_file, input_file, filename, response, text)
            except Exception as e:
                log_func(output_file, input_file, filename, f"Ошибка при обработке промпта: {e}", text)
            time.sleep(2)  # Задержка в 3 секунды после каждого запроса

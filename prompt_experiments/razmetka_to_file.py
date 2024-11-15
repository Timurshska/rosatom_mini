import os
import glob
import re
import pandas as pd

# Определение пути до последней созданной папки в директории prompt_experiments
base_dir = r'prompt_experiments/prompt_datas'
latest_folder = max(glob.glob(os.path.join(base_dir, '*')), key=os.path.getmtime)
file_path = os.path.join(latest_folder, 'prompt_result.txt')

# Проверяем существование файла
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Файл {file_path} не найден.")

# Чтение данных из txt файла
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()
# Разделение данных на блоки
blocks = re.split(r'\n\n+', content.strip())
# Парсинг блоков
data = []
for block in blocks:
    lines = block.split('\n')
    filename = lines[0].split(':')[1].strip()
    products = lines[1].split(':')[1].strip()
    products = products.split('|')  # зависит от того, что считается разделителем в промпте
    products = list(set(products))
    # Добавление каждой пары filename - product в список
    for product in products:
        if product != 'NaN':
            prod_input = product.strip().replace('\n', '')
            prod_input = prod_input.replace('\t', '')
            data.append({'File': filename, 'Product': prod_input})
df = pd.DataFrame(data)
df = df.drop_duplicates(subset=['File', 'Product'])
# Создаем маску для поиска строк со значением 'NaN'
mask = ~df.isin(['NaN']).any(axis=1)
df = df[mask]

# Создание DataFrame и запись в Excel

df.to_excel('output.xlsx', index=False)


#excel_file = 'C:/Users/Excalibur/PycharmProjects/Rosatom1/data/размеченный.xlsx'
#values = pd.read_excel(excel_file)

#values['File'] = values['File'].replace('\n', '')

#values.to_excel(excel_file, index=False) # перезаписывает исходный ф
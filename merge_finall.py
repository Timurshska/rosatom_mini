import pandas as pd
from json_repair import repair_json
import json


# Функция для объединения характеристик
def merge_characteristics(group):
    result = {}
    for characteristics in group:
        for key, value in characteristics.items():
            if key not in result:
                result[key] = value
            else:
                if isinstance(result[key], list):
                    if value not in result[key]:
                        result[key].append(value)
                elif value != result[key]:
                    result[key] = [result[key], value]
    return result

# Загрузка данных из CSV файла
df = pd.read_csv('merged.csv')
print(df.head())
# Применение функции repair_json для конвертации строк в JSON
df['Данные'] = df['Данные'].apply(repair_json)

# Конвертация JSON в словари
df['Данные'] = df['Данные'].apply(json.loads)

# Группируем строки по наименованию товара и объединяем характеристики
grouped_df = df.groupby('Предмет закупки').agg({'Данные': merge_characteristics}).reset_index()
# Выводим результат
output_file_path = 'final.csv'
grouped_df.to_csv(output_file_path, index=False)
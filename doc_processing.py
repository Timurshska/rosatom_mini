import logging
from docx import Document
from docx.table import Table

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def log_func(output_file, input_file, filename, text, text1):
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(f'filename:{filename}\n prompt_result:{text}\n')
    # with open(input_file, 'a', encoding='utf-8') as file:
    #     file.write(f'filename:{filename} prompt_input:{text1}\n')


def docx_to_txt(docx_file_path, txt_file_path):
    try:
        doc = Document(docx_file_path)
        with open(txt_file_path, "w", encoding='utf-8') as txt_file:
            _process_element(doc.element.body, txt_file)
        file_content = ""
        try:
            with open(txt_file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except:
            pass
        return file_content
    except:
        return ''


def _process_element(element, txt_file):
    for child in element:
        if isinstance(child, Table):
            for row in child.rows:
                for cell in row.cells:
                    txt_file.write(cell.text.strip() + " ")
                txt_file.write("\n")
        elif child.text:
            txt_file.write(child.text.strip() + "\n")
        else:
            _process_element(child, txt_file)  # Рекурсивный вызов для обработки вложенных элементов

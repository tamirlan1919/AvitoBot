
import re

def clean_callback_data(user_name):
    # Удаляем все специальные символы и лишние пробелы
    cleaned_data = re.sub(r'[^\w\s]', '', user_name).strip()
    # Ограничиваем длину данных до 64 символов
    cleaned_data = cleaned_data[:10]
    
    
    return cleaned_data

def gen_good_prompt_for_gpt(section: str, user_prompt, data: str = None):
    text = f'Создай подробную аналитику по разделу {section}.' \
           f'Мне нужно: {user_prompt}' \
           f'Ответ только на русском языке'
    if data:
        text += f'Данные для анализа: {data}'
    return text

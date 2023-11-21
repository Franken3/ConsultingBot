from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

SECTIONS = ["Описание продукции и области применения продукции проекта", "Сегменты рынка потребления",
            "SWOT-анализ основных товаров-заменителей", "Историческая динамика и прогноз спроса",
            "Историческая динамика и прогноз баланса спроса и экспорта",
            "Анализ транспортной и логистической инфраструктуры",
            "Анализ сторон, потенциальных возможностей и угроз на рынках  Рекомендации по ним",
            "Анализ рисков и подготовка карты рисков проекта, стресс-тестирование рынка",
            "Анализ новых проектов в данной отрасли (если возможно)", "Целевая аудитория и основные покупатели",
            "Основные барьеры входа на рынок", "Динамика рынка товаров-заменителей",
            "Расчет удельных (операционных) показателей по проекту", "Анализ рынка ключевого сырья для производства",
            "Динамика цен", "SWOT-анализ компаний производителей продукции проекта",
            "Описание и сравнение используемых производителями технологий",
            "Схема организации доставки сырья и определение оптимального транспортного плеча для доставки", ]

analitics_kb = InlineKeyboardMarkup(row_width=2)
for i in range(len(SECTIONS)):
    analitics_kb.add(InlineKeyboardButton(text=SECTIONS[i], callback_data=f'section_chose_{i}'))

start_kb = InlineKeyboardMarkup()
start_kb.add(InlineKeyboardButton(text='Начать', callback_data='show_sections'))

back_to_section_kb = InlineKeyboardMarkup()
back_to_section_kb.add(InlineKeyboardButton(text='Назад', callback_data='show_sections'))

back_to_prompt_kb = InlineKeyboardMarkup()
back_to_prompt_kb.add(InlineKeyboardButton(text='Да!', callback_data='start_analis'),
                      InlineKeyboardButton(text='Назад', callback_data='section_chose_'))


def gen_section_with_chose(ids):
    anal_kb = InlineKeyboardMarkup(row_width=2)
    for i in range(len(SECTIONS)):
        if i in ids:
            text = "✅" + SECTIONS[i]
        else:
            text = SECTIONS[i]
        anal_kb.add(InlineKeyboardButton(text=text, callback_data=f'section_chose_{i}'))
    anal_kb.add(InlineKeyboardButton(text='Перейти к промту ', callback_data=f'section_chosen'))
    return anal_kb

def continue_gen_gpt_text(msg_id, edit=False):
    continue_gen_gpt_text_kb = InlineKeyboardMarkup()
    continue_gen_gpt_text_kb.add(
        InlineKeyboardButton(text='Продолжить генерацию текста', callback_data=f'continue_gen_text_{msg_id}'),
        InlineKeyboardButton(text='Сохранить в WORD', callback_data=f'save_to_word_{msg_id}'))
    if edit:
        continue_gen_gpt_text_kb.add(
            InlineKeyboardButton(text='Изменить/Скоректировать ответ', callback_data=f'edit_prompt_{msg_id}'))
    return continue_gen_gpt_text_kb


FONTS = ["Arial", "Times New Roman", "Helvetica", "Georgia", "Courier New", "Verdana"]
PT_FONT_SIZE = [10, 12, 14, 16, 20, 22, 26, 30, 32, 34, 36, 38]
LINE_SPACING = [1, 1.2, 1.3, 1.4, 1.5, 1.7, 1.8, 1.9, 2]
ALIGNMENT = {'Левый край': 'left', 'Центр': 'center', 'Правый край': 'right'}

fonts_kb = InlineKeyboardMarkup()
for i in range(0, len(FONTS), 3):
    row_buttons = [InlineKeyboardButton(text=FONTS[j], callback_data=f'font_{j}') for j in
                   range(i, min(i + 3, len(FONTS)))]
    fonts_kb.row(*row_buttons)

pr_font_size_kb = InlineKeyboardMarkup()
for i in range(0, len(PT_FONT_SIZE), 3):
    row_buttons = [InlineKeyboardButton(text=str(PT_FONT_SIZE[j]), callback_data=f'pr_font_size_{j}') for j in
                   range(i, min(i + 3, len(PT_FONT_SIZE)))]
    pr_font_size_kb.row(*row_buttons)
pr_font_size_kb.row(InlineKeyboardButton(text='Назад', callback_data='save_to_word'))

line_spasing_kb = InlineKeyboardMarkup()
for i in range(0, len(LINE_SPACING), 3):
    row_buttons = [InlineKeyboardButton(text=str(LINE_SPACING[j]), callback_data=f'line_spasing_{j}') for j in
                   range(i, min(i + 3, len(LINE_SPACING)))]
    line_spasing_kb.row(*row_buttons)
line_spasing_kb.row(InlineKeyboardButton(text='Назад', callback_data='font_'))

alig_kb = InlineKeyboardMarkup()
alignment_keys = list(ALIGNMENT.keys())
for i in range(0, len(alignment_keys), 3):
    row_buttons = [InlineKeyboardButton(text=alignment_keys[j], callback_data=f'alig_{alignment_keys[j]}') for j in
                   range(i, min(i + 3, len(alignment_keys)))]
    alig_kb.row(*row_buttons)
alig_kb.row(InlineKeyboardButton(text='Назад', callback_data='pr_font_size_'))

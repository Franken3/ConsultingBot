from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


# Создаем новый документ

def gen_word_document(tg_id, text, pt, font, alig, line_sp):
    # Создаем новый документ
    doc = Document()

    # Добавляем параграф с заданным текстом
    paragraph = doc.add_paragraph(text)

    # Устанавливаем шрифт и размер шрифта
    run = paragraph.runs[0]
    run.font.size = Pt(pt)
    run.font.name = font

    # Устанавливаем выравнивание
    if alig == 'Левый край':
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif alig == 'Центр':
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif alig == 'Правый край':
        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Устанавливаем межстрочный интервал
    paragraph_format = paragraph.paragraph_format
    paragraph_format.line_spacing = line_sp

    # Сохраняем документ
    doc.save(f'analise_for_{tg_id}.docx')

import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery, InputFile

from keyboards.inline.callback_datas import start_kb, analitics_kb, SECTIONS, back_to_section_kb, back_to_prompt_kb, \
    continue_gen_gpt_text, fonts_kb, pr_font_size_kb, line_spasing_kb, alig_kb, FONTS, PT_FONT_SIZE, ALIGNMENT, \
    LINE_SPACING
from loader import dp, bot
from states.test import Get_Prompt
from utils.db_api.db_comands import save_user, get_assistant_answ
from utils.gpt_all.gpt import ChatGPT
from utils.gpt_all.gpt_promp_generator import gen_good_prompt_for_gpt
from utils.msword_all.msword_edit import gen_word_document


@dp.callback_query_handler(Text(startswith='save_to_word'))
async def start_analis(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.setdefault('word_params', {})
    await call.message.edit_reply_markup(reply_markup=None)
    reply_mk = fonts_kb
    await call.message.answer('Выберите шрифт:', reply_markup=reply_mk)
    await state.update_data(data)


@dp.callback_query_handler(Text(startswith='font'))
async def start_analis(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    font_id = call.data.split('_')[-1]
    if font_id.isdigit():
        data['word_params']['font_id'] = int(font_id)
    reply_mk = pr_font_size_kb
    await call.message.edit_text('Выберите размер шрифта:', reply_markup=reply_mk)
    await state.update_data(data)


@dp.callback_query_handler(Text(startswith='pr_font_size'))
async def start_analis(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    pr_font_size_id = call.data.split('_')[-1]
    if pr_font_size_id.isdigit():
        data['word_params']['pr_font_size_id'] = int(pr_font_size_id)
    reply_mk = line_spasing_kb
    await call.message.edit_text('Выберите межстрочный интервал:', reply_markup=reply_mk)
    await state.update_data(data)


@dp.callback_query_handler(Text(startswith='line_spasing'))
async def start_analis(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    line_spasing_id = call.data.split('_')[-1]
    if line_spasing_id.isdigit():
        data['word_params']['line_spasing_id'] = int(line_spasing_id)
    reply_mk = alig_kb
    await call.message.edit_text('Выберите выравнивание:', reply_markup=reply_mk)
    await state.update_data(data)


@dp.callback_query_handler(Text(startswith='alig'))
async def start_analis(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    alig_id = call.data.split('_')[-1]
    data['word_params']['alig_id'] = alig_id
    text = f"Вы выбрали:\n\n" \
           f"<b>Шрифт:</b> {FONTS[data['word_params']['font_id']]}\n\n" \
           f"<b>Размер шрифта:</b> {PT_FONT_SIZE[data['word_params']['pr_font_size_id']]}\n\n" \
           f"<b>Межстрочный интервал:</b> {LINE_SPACING[data['word_params']['line_spasing_id']]}\n\n" \
           f"<b>Выравнивание:</b> {data['word_params']['alig_id']}\n\n"
    gpt_text = await get_assistant_answ(msg_id=data['msg_id'], tg_id=call.from_user.id)
    if gpt_text is not None:
        gen_word_document(tg_id=call.from_user.id, text=gpt_text.message, pt=PT_FONT_SIZE[data['word_params']['pr_font_size_id']],
                          font=FONTS[data['word_params']['font_id']], alig=ALIGNMENT[data['word_params']['alig_id']],
                          line_sp=LINE_SPACING[data['word_params']['line_spasing_id']])
        file_path = f'analise_for_{call.from_user.id}.docx'
        await call.message.answer_document(caption=text, document=InputFile(file_path))

        # Удаление файла после отправки
        os.remove(file_path)
    else:
        await call.answer('Для этого текста уже нельзя создать файл')
    await call.message.delete()

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_datas import start_kb, analitics_kb, SECTIONS, back_to_section_kb, back_to_prompt_kb, \
    continue_gen_gpt_text, gen_section_with_chose
from loader import dp, bot
from states.test import Get_Prompt, Edit_Prompt
from utils.db_api.db_comands import save_user
from utils.gpt_all.gpt import ChatGPT
from utils.gpt_all.gpt_promp_generator import gen_good_prompt_for_gpt

gpt_instance = ChatGPT()


@dp.message_handler(CommandStart())
async def bot_start_no_state(message: Message):
    reply_mk = start_kb
    text = '<b>Добро пожаловать в бота!</b>'
    await message.answer(text, reply_markup=reply_mk)
    await save_user(message.from_user.id)
    await message.delete()


@dp.callback_query_handler(text='show_sections', state=['*'])
async def show_sections(call: CallbackQuery):
    await call.answer()
    reply_mk = analitics_kb
    text = '<b>Запрашиваю раздел</b>'
    await call.message.edit_text(text, reply_markup=reply_mk)


@dp.callback_query_handler(Text(startswith='section_chose_'), state=['*'])
async def show_sections(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.setdefault('section_id', [])
    c_data = call.data.split("_")
    if c_data[-1].isdigit():
        if int(c_data[-1]) not in data['section_id']:
            data['section_id'].append(int(c_data[-1]))
        else:
            data['section_id'].pop(data['section_id'].index(int(c_data[-1])))
    reply_mk = gen_section_with_chose(data['section_id'])
    await call.message.edit_reply_markup(reply_markup=reply_mk)
    await state.update_data(data)

@dp.callback_query_handler(Text(startswith='section_chosen'), state=['*'])
async def show_sections(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    reply_mk = back_to_section_kb

    await state.finish()

    section_text = ''
    for id in data['section_id']:
        section_text += SECTIONS[id] + "\n"
    text = f'<b>Вы выбрали разделы:</b>\n\n{section_text}\n' \
           f'<b>Напишите промпт для создания аналитики:</b>'
    msg = await call.message.edit_text(text, reply_markup=reply_mk)
    data['msg_id'] = msg.message_id

    await state.update_data(data)
    await Get_Prompt.text.set()


@dp.message_handler(state=Get_Prompt.text)
async def get_prompt(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    await state.finish()
    section_text = ''
    for id in data['section_id']:
        section_text += SECTIONS[id] + "\n"
    text = f'<b>Раздел:</b>\n\n{section_text}\n' \
           f'<b>Промпт:</b>\n\n{msg.text}\n\n' \
           f'<b>Начать аналитику?</b>'
    reply_mk = back_to_prompt_kb
    try:
        await bot.edit_message_text(message_id=data['msg_id'], chat_id=msg.from_user.id, text=text,
                                    reply_markup=reply_mk)
    except:
        await msg.answer(text=text, reply_markup=reply_mk)
    await state.update_data(data)


# продолжение генерации
@dp.callback_query_handler(text='start_analis')
async def start_analis(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await call.answer(text='Аналитика начата, я скоро пришлю вам ответ!', show_alert=True)
    msg = await call.message.edit_text(text='Здесь будет ответ!')
    await bot.send_chat_action(call.from_user.id, 'typing')
    # тут задается промт для gpt и редактируется
    # просто добавить Данные в промт и можно отправлять
    section_text = ''
    for id in data['section_id']:
        section_text += SECTIONS[id] + "\n"
    user_prompt = call.message.text.split('\n\n')[-2]
    promt = gen_good_prompt_for_gpt(section_text, user_prompt)
    gpt_answer = await gpt_instance.handle_user_message(tg_id=call.from_user.id, prompt=promt, section=section_text,
                                                        user_prompt=user_prompt, msg_id=call.message.message_id,
                                                        is_continued=False)

    reply_kb = continue_gen_gpt_text(call.message.message_id, edit=True)
    await bot.send_message(text=f'<b>Раздел</b>: {section_text}\n\n'
                                f'<b>Промпт</b>: {user_prompt}\n\n'
                                f'<b>Ответ:\n\n</b>'
                                f'{gpt_answer}', chat_id=call.from_user.id, reply_markup=reply_kb)
    await msg.delete()


@dp.callback_query_handler(Text(startswith='edit_prompt_'))
async def edit_prompt(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    c_data = call.data.split('_')
    msg_id = int(c_data[-1])
    data['msg_id'] = msg_id
    await call.message.edit_reply_markup(reply_markup=None)
    msg = await call.message.answer(text='Уточните запрос:')
    data['msg_id_u'] = msg.message_id
    await Edit_Prompt.text.set()
    await state.update_data(data)


@dp.message_handler(state=Edit_Prompt.text)
async def get_prompt(msg: Message, state: FSMContext):
    data = await state.get_data()
    promt = msg.text
    await msg.delete()
    await bot.edit_message_text(text='Здесь скоро будет уточнение', message_id=data['msg_id_u'],
                                chat_id=msg.from_user.id)
    gpt_answer = await gpt_instance.handle_user_message(tg_id=msg.from_user.id, prompt=promt, msg_id=data['msg_id'],
                                                        is_continued=True)
    reply_kb = continue_gen_gpt_text(data['msg_id'])
    await bot.edit_message_text(text=f'{gpt_answer}', chat_id=msg.from_user.id, reply_markup=reply_kb,
                                message_id=data['msg_id_u'])
    await state.finish()
    await state.update_data(data)


# продолжение генерации
@dp.callback_query_handler(Text(startswith='continue_gen_text_'))
async def start_analis(call: CallbackQuery):
    c_data = call.data.split('_')
    msg_id = int(c_data[-1])
    await call.message.edit_reply_markup(reply_markup=None)
    await call.answer('Продолжаю генерацию')
    msg = await call.message.answer(text='Здесь будет продолжение ответа!')
    promt = 'Продолжи генерацию ответа'
    gpt_answer = await gpt_instance.handle_user_message(tg_id=call.from_user.id, prompt=promt, msg_id=msg_id,
                                                        is_continued=True)
    reply_kb = continue_gen_gpt_text(msg_id)
    await bot.send_message(text=f'{gpt_answer}', chat_id=call.from_user.id, reply_markup=reply_kb)
    await msg.delete()

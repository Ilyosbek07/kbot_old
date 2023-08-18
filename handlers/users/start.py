import asyncio
import json

import asyncpg
from aiogram import types
from aiogram.types import ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.types.base import InputFile

from data.config import CHANNELS, ADMINS
from keyboards.default.all import number, menu
from keyboards.inline.all import check_button, invite_button
from loader import bot, dp, db
from states.rekStates import Number, DelUser
from utils.misc import subscription
from keyboards.default.all import menu
from keyboards.default.rekKeyboards import admin_key
from keyboards.default.rekKeyboards import back
from states.rekStates import RekData


@dp.message_handler(commands=['del'])
async def delete_user(message: types.Message, state: FSMContext):
    await message.answer('Id ni kiriting')
    await DelUser.user.set()


@dp.message_handler(text='fix', user_id=ADMINS)
async def update_scoreee(message: types.Message):
    await message.answer('id va balni kiriting')
    await Number.add_user.set()


@dp.message_handler(state=Number.add_user)
async def fixx(message: types.Message, state: FSMContext):
    user_text = message.text.split(',')
    await db.update_user_score(score=int(user_text[0]), telegram_id=int(user_text[1]))
    await message.answer('bo`ldi')
    await state.finish()


@dp.message_handler(state=DelUser.user)
async def delete(message: types.Message, state: FSMContext):
    await db.delete_users(telegram_id=int(f'{message.text}'))
    await message.answer('O"chirildi')
    await state.finish()


@dp.message_handler(commands=['upscore'])
async def delete_user(message: types.Message, state: FSMContext):
    await db.update_user_score(score=0, telegram_id=message.from_user.id)
    await message.answer('0')


@dp.message_handler(CommandStart())
async def show_channels(message: types.Message, state: FSMContext):
    args = message.get_args()
    if_old = await db.select_user(telegram_id=message.from_user.id)
    elements = await db.get_elements()
    photo = ''
    gifts = ''
    for element in elements:
        photo += f"{element['photo']}"
        gifts += f"{element['gifts']}"

    if args and not if_old:
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username
                                     )
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)
        await db.update_user_oldd(oldd='old', telegram_id=message.from_user.id)
        await db.update_user_args(user_args=f'{args}', telegram_id=message.from_user.id)

        status = True
        all = await db.select_chanel()
        chanels = []
        url = []
        channel_names = []
        for i in all:
            chanels.append(i['chanelll'])
            url.append(i['url'])
            channel_names.append(i['channel_name'])

        for channel in chanels:
            status *= await subscription.check(user_id=message.from_user.id,
                                               channel=f'{channel}')
        if status:
            user = await db.select_user(telegram_id=message.from_user.id)
            if user[3] is None or user[4] == 0:
                result = f"<b>Табриклаймиз ✅, Сиз муваффақиятли рўйхатдан ўтдингиз!</b>"
                await message.answer(result, disable_web_page_preview=True)
                await message.answer_photo(photo)
                await message.answer(text=f"{gifts}")
                await message.answer(
                    '<b>📲 Рақамни юбориш" тугмасини босган ҳолда рақамингизни юборинг!</b>',
                    reply_markup=number,
                    disable_web_page_preview=True
                )
                await Number.number.set()
            else:
                await message.answer("<b>Қуйидаги  менюдан керакли бўлимни танланг 👇</b>",
                                     reply_markup=menu, disable_web_page_preview=True)
        else:
            button = types.InlineKeyboardMarkup(row_width=1, )
            # counter = 0
            # for i in url:
            #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            #     counter += 1
            # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
            # await message.answer(
            #     '📚 Танловда иштирок этиш учун қуйидагиларга каналларга азо бўлинг.\n'
            #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            #     reply_markup=button,
            #     disable_web_page_preview=True)
            #
            button.add(
                types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
            button.add(
                types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
            button.add(
                types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
            button.add(
                types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
            counter = 0
            for i in url:
                button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
                counter += 1
            button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

            await message.answer(
                '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
                '\nКейин "✅ Азо бўлдим" тугмасини босинг',
                reply_markup=button,
                disable_web_page_preview=True)

    elif not args and not if_old:
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username

                                     )
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)
        status = True
        all = await db.select_chanel()
        chanels = []
        url = []
        channel_names = []
        for i in all:
            chanels.append(i['chanelll'])
            url.append(i['url'])
            channel_names.append(i['channel_name'])

        for channel in chanels:
            status *= await subscription.check(user_id=message.from_user.id,
                                               channel=f'{channel}')
        if status:
            user = await db.select_user(telegram_id=message.from_user.id)
            if user[3] is None or user[4] == 0:
                result = f"<b>Табриклаймиз ✅, Сиз муваффақиятли рўйхатдан ўтдингиз!</b>"
                await message.answer_photo(photo)
                await message.answer(text=f"{gifts}")
                await message.answer(
                    '<b>📲 Рақамни юбориш" тугмасини босган ҳолда рақамингизни юборинг!</b>',
                    reply_markup=number,
                    disable_web_page_preview=True
                )
                await Number.number.set()
            else:
                await message.answer("<b>Қуйидаги  менюдан керакли бўлимни танланг 👇</b>",
                                     reply_markup=menu, disable_web_page_preview=True)
        else:
            button = types.InlineKeyboardMarkup(row_width=1, )
            counter = 0
            # for i in url:
            #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            #     counter += 1
            # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
            # await message.answer(
            #     '📚 Танловда иштирок этиш учун қуйидагиларга азо бўлинг.\n'
            #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            #     reply_markup=button,
            #     disable_web_page_preview=True)
            #
            button.add(
                types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
            button.add(
                types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
            button.add(
                types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
            button.add(
                types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
            counter = 0
            for i in url:
                button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
                counter += 1
            button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

            await message.answer(
                '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
                '\nКейин "✅ Азо бўлдим" тугмасини босинг',
                reply_markup=button,
                disable_web_page_preview=True)

    else:
        try:
            user = await db.add_user(telegram_id=message.from_user.id,
                                     full_name=message.from_user.full_name,
                                     username=message.from_user.username
                                     )
        except asyncpg.exceptions.UniqueViolationError:
            user = await db.select_user(telegram_id=message.from_user.id)
        status = True
        all = await db.select_chanel()
        chanels = []
        url = []
        channel_names = []
        for i in all:
            chanels.append(i['chanelll'])
            url.append(i['url'])
            channel_names.append(i['channel_name'])

        for channel in chanels:
            status *= await subscription.check(user_id=message.from_user.id,
                                               channel=f'{channel}')
        if status:
            user = await db.select_user(telegram_id=message.from_user.id)
            if user[3] is None or user[4] == 0:
                result = f"<b>Табриклаймиз ✅, Сиз муваффақиятли рўйхатдан ўтдингиз!</b>"
                await message.answer_photo(photo)
                await message.answer(text=f"{gifts}")
                await message.answer(
                    '<b>📲 Рақамни юбориш" тугмасини босган ҳолда рақамингизни юборинг!</b>',
                    reply_markup=number,
                    disable_web_page_preview=True
                )
                await Number.number.set()
            else:
                await message.answer("<b>Қуйидаги  менюдан керакли бўлимни танланг 👇</b>",
                                     reply_markup=menu, disable_web_page_preview=True)
        else:
            button = types.InlineKeyboardMarkup(row_width=1, )
            counter = 0
            # for i in url:
            #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            #     counter += 1
            # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
            # await message.answer(
            #     '📚 Танловда иштирок этиш учун қуйидагиларга каналларга азо бўлинг.\n'
            #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            #     reply_markup=button,
            #     disable_web_page_preview=True)

            button.add(
                types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
            button.add(
                types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
            button.add(
                types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
            button.add(
                types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
            counter = 0
            for i in url:
                button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
                counter += 1
            button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

            await message.answer(
                '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
                '\nКейин "✅ Азо бўлдим" тугмасини босинг',
                reply_markup=button,
                disable_web_page_preview=True)


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    result = str()
    result2 = str()
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])
    elements = await db.get_elements()
    photo = ''
    gifts = ''
    for element in elements:
        photo += f"{element['photo']}"
        gifts += f"{element['gifts']}"

    for channel in chanels:
        status *= await subscription.check(user_id=call.from_user.id,
                                           channel=f'{channel}')
    if status:
        if_old = await db.select_user(telegram_id=call.from_user.id)
        if if_old[3] is None or if_old[4] == 0:
            result += f"<b>Табриклаймиз ✅, Сиз муваффақиятли рўйхатдан ўтдингиз!</b>"
            await call.message.answer(result, disable_web_page_preview=True)
            await call.message.answer_photo(photo=photo)
            await call.message.answer(text=f"{gifts}")
            await call.message.answer(
                '<b>📲 Рақамни юбориш" тугмасини босган ҳолда рақамингизни юборинг!</b>',
                reply_markup=number,
                disable_web_page_preview=True
            )
            await Number.number.set()
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            await call.message.answer("<b>Қуйидаги  менюдан керакли бўлимни танланг 👇</b>",
                                      reply_markup=menu, disable_web_page_preview=True)

    else:
        result2 += (f"<b>❌ Каналга аъзо бўлмадингиз!\n"
                    f"Ботдан тўлиқ фойдаланиш учун кўрсатилган барча каналларга аъзо бўлинг!</b>")
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        # for i in url:
        #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
        #     counter += 1
        # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
        # await call.message.answer(result2)
        # await call.message.answer(
        #     '📚 Танловда иштирок этиш учун қуйидагиларга азо бўлинг.\n'
        #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
        #     reply_markup=button,
        #     disable_web_page_preview=True)
        button.add(
            types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
        button.add(
            types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
        button.add(
            types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
        button.add(
            types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

        await call.message.answer(
            '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
            '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            reply_markup=button,
            disable_web_page_preview=True)


@dp.message_handler(state=Number.number, content_types=types.ContentType.CONTACT)
async def phone_number(message: types.Message, state: FSMContext):
    elements = await db.get_elements()
    scoree = 0
    for element in elements:
        scoree += element['limit_score']

    user = await db.select_user(telegram_id=message.from_user.id)
    numberr = f'{message.contact.phone_number}'
    if numberr.startswith("+998") or numberr.startswith("998"):
        if user[3] is None or user[4] == 0:
            try:
                user_telephone_num = await db.update_user_phone(phone=message.contact.phone_number,
                                                                telegram_id=message.from_user.id)
            except:
                pass
            if user[4] == 0 or user[4] is None:
                user = await db.update_user_score(score=scoree, telegram_id=message.from_user.id)
            try:
                args = await db.select_user(telegram_id=message.from_user.id)
                args_user = await db.select_user(telegram_id=int(args[7]))

                update_score = int(args_user[4]) + scoree
                await db.update_user_score(score=update_score, telegram_id=int(args[7]))
                await bot.send_message(chat_id=int(args[7]),
                                       text=f"👤 Йанги иштирокчи кушилди\n"
                                            f"🎗 Сизнинг балингиз {update_score},"
                                            f" кўпроқ дўстларингизни таклиф этиб баллингизни оширинг!")
            except Exception as e:
                pass
            await message.answer(f"<b>🎉 Табриклаймиз! Сиз бошланғич {scoree} баллга эга бўлдингиз!</b>",
                                 disable_web_page_preview=True)
            await message.answer("<b>Қуйидаги  менюдан керакли бўлимни танланг 👇</b>",
                                 reply_markup=menu, disable_web_page_preview=True)
            await state.finish()
        else:
            await message.answer("<b>Қуйидаги  менюдан керакли бўлимни танланг 👇</b>",
                                 reply_markup=menu, disable_web_page_preview=True)
            await state.finish()
    else:
        await message.answer('Kechirasiz Faqat O`zbekiston raqamlarini qabul qilamiz',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(text='🎁 ТАНЛОВДА ИШТИРОК ЭТИШ')
async def tanlov(message: types.Message):
    elements = await db.get_elements()
    photo = ''
    txt = ''
    for element in elements:
        photo += f"{element['photo']}"
        txt += f"{element['game_text']}"

    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])

    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        txt += f'\n\nhttp://t.me/parvoziy_bot?start={message.from_user.id}'
        await message.answer_photo(photo=photo,
                                   caption=txt
                                   )
        await message.answer(
            '👆 Юқоридаги сизнинг <b>реферал</b> линк/ҳаволангиз. Уни кўпроқ танишларингизга улашинг. Омад!')

    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        # for i in url:
        #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
        #     counter += 1
        # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
        #
        # await message.answer(
        #     '📚 Танловда иштирок этиш учун қуйидагиларга азо бўлинг.\n'
        #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
        #     reply_markup=button,
        #     disable_web_page_preview=True)
        button.add(
            types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
        button.add(
            types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
        button.add(
            types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
        button.add(
            types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

        await message.answer(
            '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
            '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            reply_markup=button,
            disable_web_page_preview=True)


@dp.message_handler(text='🎁 Совғалар')
async def my_score(message: types.Message):
    elements = await db.get_elements()
    photo = ''
    txt = ''
    for element in elements:
        photo += f"{element['photo']}"
        txt += f"{element['gifts']}"

    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])
    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        await message.answer_photo(photo)
        await message.answer(text=txt)

    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        # for i in url:
        #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
        #     counter += 1
        # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
        #
        # await message.answer(
        #     '📚 Танловда иштирок этиш учун қуйидагиларга азо бўлинг.\n'
        #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
        #     reply_markup=button,
        #     disable_web_page_preview=True)
        button.add(
            types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
        button.add(
            types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
        button.add(
            types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
        button.add(
            types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

        await message.answer(
            '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
            '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            reply_markup=button,
            disable_web_page_preview=True)


@dp.message_handler(text='Statistika 📊')
async def show_users(message: types.Message):
    a = await db.count_users()
    await message.answer(f'<b>🔷 Жами обуначилар: {a} та</b>')


@dp.message_handler(text='👤 Балларим')
async def my_score(message: types.Message):
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])

    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        try:
            score = await db.select_user(telegram_id=message.from_user.id)
            await message.answer(f'<b>Сизда {score[4]} - балл мавжуд</b>')
        except Exception as err:
            await message.answer('Iltimos /start ni bosing')
    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        # for i in url:
        #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
        #     counter += 1
        # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
        #
        # await message.answer(
        #     '📚 Танловда иштирок этиш учун қуйидагиларга азо бўлинг.\n'
        #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
        #     reply_markup=button,
        #     disable_web_page_preview=True)
        #
        button.add(
            types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
        button.add(
            types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
        button.add(
            types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
        button.add(
            types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

        await message.answer(
            '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
            '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            reply_markup=button,
            disable_web_page_preview=True)


#

# @dp.message_handler(text='🧑🏻‍💻 Админ')
# async def admin(message: types.Message):
#     status = True
#     for channel in CHANNELS:
#         status *= await subscription.check(user_id=message.from_user.id,
#                                            channel=channel)
#     if status:
#         await message.answer(f'@Dilshodbek_Zubaydov1')
#     else:
#         await message.answer(f'Танловда иштирок этиш учун қуйидаги 6 каналга аъзо бўлинг. '
#                              f'Кейин "Аъзо бўлдим" тугмасини босинг',
#                              reply_markup=check_button,
#                              disable_web_page_preview=True)


@dp.message_handler(text='📊 Рейтинг')
async def score(message: types.Message):
    status = True
    all = await db.select_chanel()
    chanels = []
    url = []
    channel_names = []
    for i in all:
        chanels.append(i['chanelll'])
        url.append(i['url'])
        channel_names.append(i['channel_name'])
    for channel in chanels:
        status *= await subscription.check(user_id=message.from_user.id,
                                           channel=f'{channel}')
    if status:
        try:
            ball = await db.select_user(telegram_id=message.from_user.id)
            counter = 1
            text = '📊 Ботимизга энг кўп дўстини таклиф қилиб балл тўплаганлар рўйҳати: \n\n'
            elements = await db.get_elements()
            winners = 0

            for i in elements:
                winners += int(i["winners"])
            top = await db.select_top_users(lim_win=winners)
            for i in top:
                text += f"🏅{counter}-o'rin   {i[1]} • {i[4]} ball\n"
                counter += 1
            if counter:
                text += f'\n\n✅ Сизда {ball[4]} балл \nкўпроқ дўстларингизни таклиф этиб баллингизни оширинг!'
                await bot.send_message(chat_id=message.from_user.id, text=text, parse_mode="")
        except Exception as err:
            await bot.send_message(chat_id=935795577, text=f"{err}")
            await message.answer('Iltimos /start ni bosing')

    else:
        button = types.InlineKeyboardMarkup(row_width=1, )
        counter = 0
        # for i in url:
        #     button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
        #     counter += 1
        # button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))
        #
        # await message.answer(
        #     '📚 Танловда иштирок этиш учун қуйидагиларга азо бўлинг.\n'
        #     '\nКейин "✅ Азо бўлдим" тугмасини босинг',
        #     reply_markup=button,
        #     disable_web_page_preview=True)
        button.add(
            types.InlineKeyboardButton(text='𝓐𝓼𝓪𝓵"𝓼_𝓑𝓵𝓸𝓰 📚💞', url="https://t.me/+1kFU1nYz8543MGVi"))
        button.add(
            types.InlineKeyboardButton(text="KABIRANING KUNDALIGI", url="https://t.me/+CawlXbOkI1o0MDli"))
        button.add(
            types.InlineKeyboardButton(text="Solihah....", url="https://t.me/+ljVF1T7rYu5hZmYy"))
        button.add(
            types.InlineKeyboardButton(text="Furqoniyyaة", url="https://t.me/+Wctln7Cdzfk2Mjhi"))
        counter = 0
        for i in url:
            button.add(types.InlineKeyboardButton(f"{channel_names[counter]}", url=f'https://t.me/{i}'))
            counter += 1
        button.add(types.InlineKeyboardButton(text="✅ Азо бўлдим", callback_data="check_subs"))

        await message.answer(
            '🎁 Танловда иштирок этиш учун қуйидагиларга 1-4 каналларга азо бўлиш сўровини юборинг ва колган каналга азо бўлинг.\n'
            '\nКейин "✅ Азо бўлдим" тугмасини босинг',
            reply_markup=button,
            disable_web_page_preview=True)


@dp.message_handler(text='💡 Шартлар')
async def help(message: types.Message):
    elements = await db.get_elements()
    photo = ''
    shartlar = ''
    for element in elements:
        photo += f"{element['photo']}"
        shartlar += f"{element['shartlar']}"
    await message.answer_photo(caption=shartlar, photo=photo)


@dp.message_handler(Command('jsonFile'))
async def jsonnn(message: types.Message):
    user_list = []
    userss = await db.select_all_users()
    for user in userss:
        user_dict = {}
        user_dict['full_name'] = user[1]
        user_dict['username'] = user[2]
        user_dict['phone'] = user[3]
        user_dict['score'] = user[4]
        user_dict['tg_id'] = user[6]
        user_list.append(user_dict)
        await asyncio.sleep(0.05)
    with open("users.json", "w") as outfile:
        json.dump(user_list, outfile)
    document = open('users.json')
    await bot.send_document(message.from_user.id, document=document)


@dp.message_handler(text="G'oliblar haqida ma'lumot")
async def scoree(message: types.Message):
    try:
        counter = 1
        text = '📊 Ботимизга энг кўп дўстини таклиф қилиб балл тўплаганлар рўйҳати: \n\n'
        elements = await db.get_elements()
        winners = 0

        for i in elements:
            winners += int(i["winners"])
        top = await db.select_top_users(lim_win=winners)
        for i in top:
            text += f"🏅{counter}-o'rin  {i[1]} • {i[4]} ball , username: @{i[2]} , phone: {i[3]}, telegram_id: {i[6]}\n "
            counter += 1
        if counter:
            await message.answer(text=text, parse_mode="")

    except Exception as err:
        await bot.send_message(chat_id=935795577, text=f"{err}")
        await message.answer('Iltimos /start ni bosing')


@dp.message_handler(Command('read_file'))
async def json_reader(message: types.Message):
    f = open('users.json', 'r')
    data = json.loads(f.read())
    for user in data:
        print(user['tg_id'])
        try:
            user = await db.add_json_file_user(
                telegram_id=user['tg_id'],
                username=user['username'],
                full_name=user['full_name'],
                phone=user['phone'],
                score=user['score']
            )
        except Exception as e:
            print(e)
    f.close()


@dp.message_handler(commands=['dasturchi'])
async def i_2(message: types.Message):
    image = 'https://telegra.ph/file/b3033779713cd505f421b.jpg'
    await message.answer_photo(
        photo=image,
        caption='📈 Telegram bot xizmatlarini taklif qilamiz.\n\n'
                'Siz ham ozingiz uchun shunday botlarga ega bo`lishni istasangiz bizga murojaat qiling \n\n'
                '‍💻 Dasturchi: @Ilyosbek_Kv\n 📄Batafsil: @texnohelpuz\n\n'
                'Arab tili va Islomiy kinolarga qiziquvchilar uchun @islomiy_ilmlar_robot')

# @dp.message_handler(commands=['dasturchi'])
# async def i_2(message: types.Message):
# image = InputFile(path_or_bytesio='111.jpg')
# await message.answer_photo(
#     photo=image,
#     caption=\
# await message.answer('📈 Telegram bot xizmatlarini taklif qilamiz.\n\n'
#             'Siz ham ozingiz uchun shunday botlarga ega bo`lishni istasangiz bizga murojaat qiling \n\n'
#             '‍💻 Dasturchi: @Ilyosbek_Kv\n 📄Batafsil: @texnohelpuz\n\n'
#             'Arab tili va Islomiy kinolarga qiziquvchilar uchun @islomiy_ilmlar_robot')

from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from keyboards.default.all import menu
from keyboards.default.rekKeyboards import admin_key
from keyboards.default.rekKeyboards import back
from loader import dp, db
from states.rekStates import RekData


@dp.message_handler(commands=['admin'], user_id=ADMINS)
async def admin(message: types.Message):
    await message.answer(text='Admin panel',
                         reply_markup=admin_key)


@dp.message_handler(text='Kanal ➕', user_id=ADMINS)
async def add_channel(message: types.Message):
    await message.answer(text='Kanalni kiriting\n\n'
                              'Masalan : "@Chanel zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                         reply_markup=back)
    await RekData.add.set()


@dp.message_handler(state=RekData.add)
async def add_username(message: types.Message, state: FSMContext):
    text = message.text
    if text[0] == '@':
        text_split = text.split(',')

        await db.add_chanell(chanelll=f"{text_split[0]}",
                             channel_name=f"{text_split[1]}", url=f"{text_split[0][1:]}")
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()
    elif text == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()
    elif text[0] == '-':
        split_chanel = message.text.split(',')
        chanel_lst = []
        url_lst = []
        channel_name_lst = []
        for i in split_chanel:
            lst = i.split('and')
            chanel_lst.append(lst[0])
            url_lst.append(lst[1])
            channel_name_lst.append(lst[2])
        chanel = f'{chanel_lst}'
        url = f'{url_lst}'
        channel_name = f'{url_lst}'
        ch_text = chanel.replace("'", '')
        ch_text2 = ch_text.replace(" ", '')
        u_text = url.replace("'", '')
        u_text2 = u_text.replace(" ", '')
        channel_name_text = channel_name.replace("'", '')
        channel_name_text2 = channel_name_text.replace(" ", '')

        await db.add_chanell(chanelll=ch_text2[1:-1], url=u_text2[1:-1],channel_name=channel_name_text2[1:-1])
        await message.answer("Qo'shildi", reply_markup=admin_key)
        await state.finish()

    else:
        await message.answer('Xato\n\n'
                             '@ belgi bilan yoki kanal id(-11001835334270andLink) sini link bilan birga kiriting kiriting')


@dp.message_handler(text='Kanal ➖', user_id=ADMINS)
async def add_channel(message: types.Message):
    await message.answer(text='Kanalni kiriting @ belgi bilan\n\n'
                              'Masalan : "Kanal zayavkada bo`lsa chanel_id(-123123213),chanel_url"\n\n',
                         reply_markup=back)
    await RekData.delete.set()


@dp.message_handler(state=RekData.delete)
async def del_username(message: types.Message, state: FSMContext):
    txt = message.text
    if txt[0] == '-':
        chanel = await db.get_chanel(channel=txt)
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()

        # await message.answer("O'chirildi")
        # await state.finish()
    elif txt[0] == '@':
        chanel = await db.get_chanel(channel=f"{txt}")
        if not chanel:
            await message.answer("Kanal topilmadi\n"
                                 "Qaytadan urinib ko'ring")

        else:
            await db.delete_channel(chanel=txt)
            await message.answer('Kanal o"chirildi', reply_markup=admin_key)
            await state.finish()
    elif txt == '🔙️ Orqaga':
        await message.answer('Admin panel', reply_markup=admin_key)
        await state.finish()


# @dp.message_handler(text='Statistika 📊')
# async def show_users(message: types.Message):
#     a = await db.count_users()
#     await message.answer(f'<b>🔷 Жами обуначилар: {a} та</b>')


@dp.message_handler(text='🏘 Bosh menu')
async def menuu(message: types.Message):
    await message.answer('Bosh menu', reply_markup=menu)


@dp.message_handler(text='Kanallar 📈')
async def channels(message: types.Message):
    channels = await db.select_chanel()
    text = ''
    for channel in channels:
        text += f"{channel['chanelll']}\n"
    try:
        await message.answer(f"{text}", reply_markup=admin_key)
    except:
        await message.answer(f"Kanallar mavjud emas")


@dp.message_handler(text='Hisobni 0 ga tushirish')
async def channels(message: types.Message):
    try:
        await db.update_users_all_score()
        await message.answer(f"Hisoblar 0 ga tushirildi", reply_markup=admin_key)
    except Exception as err:
        await message.answer(f"Muammo yuzaga keldi\n\n{err}")


@dp.message_handler(text='Rasmni almashtirish 🖼')
async def change_picture(message: types.Message):
    await message.answer('Rasmni kiriting', reply_markup=back)
    await RekData.picture.set()


@dp.message_handler(content_types=['photo', 'text', 'video'], state=RekData.picture)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1].file_id
        elements = await db.get_elements()
        if elements:
            await db.update_photo(photo=photo)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()

        else:
            await db.add_photo(photo=photo)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()
    elif message.text == '/start':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()

    else:
        await message.answer('Faqat rasm qabul qilamiz')


@dp.message_handler(text="O'yin haqida matn 🎮")
async def change_picture(message: types.Message):
    await message.answer('Textni kiriting', reply_markup=back)
    await RekData.text.set()


@dp.message_handler(state=RekData.text)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if elements:
            await db.update_game_text(game_text=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        else:
            await db.add_text(game_text=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()
    else:
        await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="Sovg'alar ro'yxatini kiritish 📄")
async def change_picture(message: types.Message):
    await message.answer('Textni kiriting', reply_markup=back)
    await RekData.gift.set()


@dp.message_handler(state=RekData.gift)
async def change_picture_(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if elements:
            await db.update_gift(gift=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        else:
            await db.add_gift(gift=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()
    else:
        await message.answer('Faqat Text qabul qilamiz')


@dp.message_handler(text="Taklif miqdorini kiritish 🎁")
async def change_picture(message: types.Message):
    await message.answer('Faqat son kiriting', reply_markup=back)
    await RekData.score.set()


@dp.message_handler(state=RekData.score)
async def change_picture_(message: types.Message, state: FSMContext):
    try:
        text = int(message.text)

        if text:
            elements = await db.get_elements()
            if elements:
                await db.update_limit_score(limit_score=text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()
            # else:
            # await db.add_text()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
    except:
        if message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
        else:
            await message.answer('Faqat Son qabul qilamiz')


@dp.message_handler(text='Shartlarni qo"shish 🖼')
async def shartlar(message: types.Message):
    await message.answer('Shartlarni kiriting', reply_markup=back)
    await RekData.kbsh.set()


@dp.message_handler(state=RekData.kbsh)
async def shartlarr(message: types.Message, state: FSMContext):
    if message.text:
        elements = await db.get_elements()
        if message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        if elements:
            await db.update_shartlar(shartlar=message.text)
            await message.answer('Yangilandi', reply_markup=admin_key)
            await state.finish()

        else:
            await db.add_shartlar(shartlar=message.text)
            await message.answer('Qo`shildi', reply_markup=admin_key)
            await state.finish()

    elif message.text == '🔙️ Orqaga':
        await message.answer('Bosh menu', reply_markup=menu)
        await state.finish()
    else:
        await message.answer('Faqat text qabul qilamiz')


@dp.message_handler(text="G'oliblar sonini kirting")
async def change_picture(message: types.Message):
    await message.answer('Faqat son kiriting', reply_markup=back)
    await RekData.winners.set()


@dp.message_handler(state=RekData.winners)
async def change_picture_(message: types.Message, state: FSMContext):
    try:
        text = int(message.text)
        if message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        if text:
            elements = await db.get_elements()
            if elements:
                await db.winners(winners=text)
                await message.answer('Yangilandi', reply_markup=admin_key)
                await state.finish()

        elif message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
    except Exception as err:

        if message.text == '🔙️ Orqaga':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()
        elif message.text == '/start':
            await message.answer('Bosh menu', reply_markup=menu)
            await state.finish()

        else:
            await message.answer('Faqat Son qabul qilamiz')

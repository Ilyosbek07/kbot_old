from aiogram import executor

from loader import dp, db
from handlers.users import start
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()
    await db.drop_Chanel()
    await db.create_table_chanel()
    await db.create_table_testtt()
    await db.create_table_users()
    await db.create_table_chanel_element()

    await set_default_commands(dispatcher)

    # scheduler = AsyncIOScheduler(timezone='Asia/Tashkent')

    # scheduler.add_job(start.send, trigger='interval', seconds=60, kwargs={'bot': Bot})
    # scheduler.add_job(start.jsonn, trigger='interval', days=11)
    # scheduler.start()

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

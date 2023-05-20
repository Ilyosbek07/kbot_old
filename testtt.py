# import aiohttp
# import asyncio
#
# # @dp.message_handler(text='Test')
# # async def add_channel(message: types.Message):
# #     await message.answer(text='url',
# #                          )
# #     await RekData.ttttt.set()
# #
# # @dp.message_handler(state=RekData.ttttt)
# # async def ttttttt(message: types.Message, state: FSMContext):
# #     chat_id = message.chat.id
# #     url = message.text
# #     yt = YouTube(url)
# #     if message.text.startswith == "https://www.youtube.com/" or 'http://www.youtube.com':
# #         await bot.send_message(chat_id, f"*yuklanmoqda*: *{yt.title}*)",
# #                                parse_mode="Markdown")
#         # await download_youtube_video(url, message, bot)
# #
# #
# # async def download_youtube_video(url, message, bot):
# #     yt = YouTube(url)
# #     stream = yt.streams.filter(progressive=True, file_extension='mp4')
# #     stream.get_highest_resolution().download(f'{message.chat.id}', f'{message.chat.id}_{yt.title}')
# #     with open(f"{message.chat.id}/{message.chat.id}_{yt.title}", 'rb') as video:
# #         await bot.send_video(message.chat.id, video, caption='botimiz orqali yuklab olindi', parse_mode='Markdown')
# #         os.remove(f"{message.chat.id}/{message.chat.id}_{yt.title}")
#
# async def fetch_video_data(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 print(response)
#                 video_data = await response.content()
#                 print(video_data)
#                 # Process the video data as needed
#             else:
#                 print(f"Error fetching video: {response.status}")
#
#
# # Call the fetch_video_data function asynchronously
# asyncio.run(fetch_video_data("https://u6876.xvest2.ru/Allsave/AllsaveApi.php?url=https://youtu.be/IUMgR0CsfU8"))

import requests
import json

response = requests.request("GET", 'https://u6876.xvest2.ru/Allsave/AllsaveApi.php?url=https://youtu.be/IUMgR0CsfU8')
r = json.loads(response.content)
data = ['url']['url']
# video_quality data = r['video_quality']
# rasm data = r['thumb']
print(data)
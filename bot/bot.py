import csv
import os
import textwrap
import time
from copy import deepcopy

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from environs import Env
from loguru import logger

from database.database import dict_new, dict_old
from parser_shadow import lets_pars_shadow
from pars_trans import lets_pars_trans

env = Env()
env.read_env()

bot: Bot = Bot(token=env('BOT_TOKEN'))
dp: Dispatcher = Dispatcher()
user_id: int = env('USER_ID')


def check_sr(sr: dict, tr: dict):
    # те, кого сейчас нет в файле с травмами, на проверку
    added = sr.keys() - tr.keys()
    # те, кто сейчас есть в файле с травмами, но нет на СР по фильтру травмы, на проверку
    removed = tr.keys() - sr.keys()
    # те, кто есть и там и там, пересечение множеств
    injury_names = sr.keys() & tr.keys()
    # делаем словарь точно травмированных, в формате имя-ссылка
    injury = {name: tr[name] for name in injury_names}

    for player in added:
        tr_injury = lets_pars_trans(player)
        # если травма на ТР есть, то добавляем его в список травмированных
        if tr_injury:
            injury[player] = sr[player]

    for player in removed:
        tr_injury = lets_pars_trans(player)
        # если травмы нет, то убираем его из списка травмированных
        if tr_injury:
            injury[player] = tr[player]

    return injury


def return_changes(dict_n: dict, dict_o: dict):

    # вычилсяем, кто добавлен по ключам, из ключей нового словаря вычитаем ключи старого словаря
    added = dict_n.keys() - dict_o.keys()
    # вычилсяем, кто выбыл по ключам, из ключей старого словаря вычитаем ключи нового словаря
    removed = dict_o.keys() - dict_n.keys()

    added_dict = dict()
    removed_dict = dict()

    # составляем словарь добавленных игроков, ключ-имя, значение-ссылка
    for player in added:
        added_dict[player] = dict_n[player]

    # составляем словарь выбывших игроков, ключ-имя, значение-ссылка
    for player in removed:
        removed_dict[player] = dict_o[player]

    if added_dict != {} and removed_dict == {}:
        return f'Добавлены следующие игроки:\n\n{added_dict}.\n\nНикто не выбыл.'
    elif added_dict == {} and removed_dict != {}:
        return f'Выбыли следующие игроки:\n\n{removed_dict}.\n\nНикто не добавлен.'
    elif added_dict == {} and removed_dict == {}:
        # return 'Изменений нет'
        return None
    return f'Добавлены следующие игроки:\n\n{added_dict}.\n\nВыбыли следующие игроки:\n\n{removed_dict}.'


@dp.message(CommandStart())
async def process_start_command(message: Message):
    name = message.from_user.full_name
    await message.answer(text=f'Привет, {name}! Бот запущен')
    await bot.send_message(chat_id=user_id, text='Бот запущен')
    
    logger.add('../bot/debugs/debug.log', format='{time} {level} {message}', level='DEBUG', rotation='10:00')

    time.sleep(5)

    while True:
        # print('Проверяем наличие файла с игроками')
        logger.debug('Проверяем наличие файла с игроками')
        try:
            if os.path.isfile("files/res_trans.csv"):
                with open("files/res_trans.csv", 'r', encoding='utf-8') as f:
                    file_content = [line.strip() for line in f.readlines()]
                    dict_old.clear()

                    for line in file_content:
                        line_x = line.split(';')
                        dict_old[line_x[0].replace('\ufeff', '')] = line_x[1]
        except Exception as e:
            await bot.send_message(chat_id=user_id, text='Возникла ошибка при проверке старого файла ' + type(e).__name__ + str(e))

        # print('Запускаем парсер')
        logger.debug('Запускаем парсер')
        try:
            lets_pars_shadow()
        except Exception as e:
            logger.error(type(e).__name__ + str(e))
            await bot.send_message(chat_id=user_id, text='Возникла ошибка при парсинге ' + type(e).__name__ + str(e))

        time.sleep(5)

        # print('Считываем инфу с парсера')
        logger.debug('Считываем инфу с парсера')
        try:
            with open("files/res.csv", 'r+', encoding='utf-8', newline='') as f:
                dict_new.clear()

                file_content = [line.strip() for line in f.readlines()]

                for line in file_content:
                    line_x = line.split(';')
                    dict_new[line_x[0].replace('\ufeff', '')] = line_x[1]

        except Exception as e:
            logger.error(type(e).__name__ + str(e))
            await bot.send_message(chat_id=user_id, text='Возникла ошибка при чтении результатов парсинга и сравнении со старым файлом ' + type(e).__name__ + str(e))

        try:
            # print('Сравниваем результат сайта СР с сайтом ТР')
            logger.debug('Сравниваем результат сайта СР с сайтом ТР')
            injury = check_sr(dict_new, dict_old)
        except Exception as e:
            injury = deepcopy(dict_old)
            logger.error(type(e).__name__ + str(e))
            await bot.send_message(chat_id=user_id, text='Возникла ошибка при Сравниваем результат сайта СР с сайтом ТР ' + type(e).__name__ + str(e))

        try:
            # print('Делаем сравнение с предыдущим парсингом')
            logger.debug('Делаем сравнение с предыдущим парсингом')
            answer = return_changes(injury, dict_old)
        except Exception as e:
            logger.error(type(e).__name__ + str(e))
            await bot.send_message(chat_id=user_id, text='Возникла ошибка при сравнение с предыдущим парсингом ' + type(e).__name__ + str(e))

        try:
            # print('Записываем данные из словаря injury в файл')
            logger.debug('Записываем данные из словаря injury в файл')
            with open('files/res_trans.csv', 'w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                for n, p_l in injury.items():
                    writer.writerow([n, p_l])
        except Exception as e:
            logger.error(type(e).__name__ + str(e))
            await bot.send_message(chat_id=user_id, text='Возникла ошибка при Записываем данные из словаря injury в файл ' + type(e).__name__ + str(e))

        # print('Отправляем сообщение пользователю')
        logger.debug('Отправляем сообщение пользователю')
        try:
            if answer is not None:
                if len(answer) > 4000:
                    parts = textwrap.wrap(answer, width=4000)
                    for part in parts:
                        await message.answer(text=part)
                        await bot.send_message(chat_id=user_id, text=part)
                else:
                    await message.answer(text=answer)
                    await bot.send_message(chat_id=user_id, text=answer)

        except Exception as e:
            logger.error(type(e).__name__ + str(e))
            await bot.send_message(chat_id=user_id, text='Возникла ошибка при отправке сообщения с результатом ' + type(e).__name__ + str(e))

        time.sleep(60)


# @dp.message(F.document)
# async def process_sent_document(message: Message):
#
#     dict_new.clear()
#
#     file_id = message.document.file_id
#     file = await bot.get_file(file_id)
#     file_path = file.file_path
#
#     await bot.download_file(file_path, "files/text.csv")
#
#     with open("files/text.csv", 'r', encoding='utf-8') as f:
#         file_content = [line.strip() for line in f.readlines()]
#
#         # for line in file_content:
#         #     name, url = line.split(';')
#         #
#         #     await message.answer(text=f'{name} ссылка {url}')
#         for line in file_content:
#             line_x = line.split(';')
#             dict_new[line_x[0].replace('\ufeff', '')] = line_x[1]
#
#         answer = return_changes(dict_new, dict_old)
#
#         for line in file_content:
#             line_x = line.split(';')
#             dict_old[line_x[0].replace('\ufeff', '')] = line_x[1]
#
#     await message.answer(text=answer)


if __name__ == '__main__':
    dp.run_polling(bot)

from aiogram import Bot, Dispatcher, executor, types
import configgu,logging,random,wikipedia

"""Причина выбора aiogram: 
Асинхронность позволяет ускорять работу нашего бота"""

#Объект бота
bot = Bot(token=configgu.config['token'])

"""############### ФУНКЦИЯ ДЛЯ ПОИСКА ЗАПРОСА В ВИКИПЕДИИ ##################"""
def wiki(search):
    wikipedia.set_lang("ru")
    try: #Обработка исключений
        page = wikipedia.page(search)  # Делаем запрос
        page_1000 = page.summary[:1000] #Первая 1000 символов,дабы предотвратить ошибку
        page_1000 = page_1000.split('.') #Разделяем по предложениям
        del page_1000[-1] #Убираем кусок незаконченного предложения с конца
        page_1000 = ".".join(page_1000) + '.' #Восстанавливаем полный текст,добавляя точки
        return page_1000
    except: #Если ничего не нашёл
        return "🚫 Wikipedia не нашла информацию по вашему запросу 🚫"


#Диспетчер бота для команд
dp = Dispatcher(bot)

#Включаем логи чтобы ничего не упустить
logging.basicConfig(level=logging.INFO)

"""############### БЛОК КОМАНД БОТА ##################"""

#Реакция на команду /start
@dp.message_handler(commands=["start"])
async def startt(message: types.Message): #Используем message для краткой записи types.Message
    try:
        sticker = open('sticker.webp', 'rb')  # Открываем стикер приветствия
        await bot.send_sticker(message.chat.id,sticker)
        await message.delete()
    except:
        await message.reply('Добавь бота в свою личку:\nhttps://t.me/SSSENKABOT')

    # Внизу преветствующее сообщение с имеенем юзера и именем бота + отправка его пользователю
    messag = f'Привет <u>{message.from_user.full_name}</u>,меня зовут <b>SENATT BOT</b>\nСкорее пиши /help и узнай все мои возможности!'
    await bot.send_message(message.chat.id,messag,parse_mode='html')

#Реакция на команду /help
@dp.message_handler(commands=["help"])
async def helpp(message:types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)  # Создали разметку на три кнопки в каждом ряду + подрегулировали размер
    randomch = types.KeyboardButton('♾ Рандомное число')  # Кнопка №1
    sitec = types.KeyboardButton('Сайт XAKER')  # Кнопка №2
    dice = types.KeyboardButton('🎲 Игральная кость')  # Кнопка №3
    ID_user = types.KeyboardButton('🆔')  # Кнопка №4
    photo_user = types.KeyboardButton('📸 Photo')  # Кнопка №5
    how_are_you = types.KeyboardButton('✌ Как дела?') # Кнопка №6
    wiki = types.KeyboardButton('🔍 Википедия')  # Кнопка №7
    stop = types.KeyboardButton('🛑 Stop')  # Кнопка №8

    markup.add(randomch,sitec,dice,ID_user,photo_user,how_are_you,wiki,stop)

    await bot.send_message(message.chat.id,'У меня есть несколько встроенных команд:',reply_markup=markup)
    await message.delete()

#Реакция на команду /stop
@dp.message_handler(commands=["stop"])
async def stopp(message: types.Message):
    await dp.stop_polling()
    await message.delete()


"""############### КЛИЕНТСКАЯ ЧАСТЬ ##################"""

@dp.message_handler(content_types=['new_chat_members']) #если присоединился новый пользователь
async def neww(message:types.Message):
    print('JOINED NEW USER') #уведомляет в консоль
    await message.delete() #удаляет из чата оповещение о новом вхождении участника

@dp.callback_query_handler(text=["good","bad"]) #Реакция на нажатие кнопки InlineKeyboardMarkup
async def callback(call: types.CallbackQuery):
    if call.data == "good": #Если положительный,то
        await call.message.answer("🔥 Огонь,бро") #Ответ бота
        await call.message.edit_reply_markup() #Удаляем кнопки вариантов ответа
    elif call.data == "bad": #Если отрицательный,то
        await call.message.answer("😢") #Ответ бота
        await call.message.edit_reply_markup() #Удаляем кнопки вариантов ответа


@dp.message_handler(content_types=['text'])
async def textt(message: types.Message):
    if message.text == '🆔':  # Если ввёл ID
        # Получи свой ID
        await bot.send_message(message.chat.id, f'Твой ID: <b>{message.from_user.id}</b>', parse_mode='html')


    elif 'photo' in message.text.lower():  # Открывает фото-файл и отсылает вам
        photof = open('photof.jpg', 'rb')
        await bot.send_photo(message.chat.id, photof)

    elif 'рандомное число' in message.text.lower():  # С помощью модуля random генерирует числа от 0 до 99
        await bot.send_message(message.chat.id, f'{random.randint(0, 100)}')

    elif message.text.lower() == 'сайт xaker':  # Высылает текст + кнопку-ссылку для перехода на него
        markup = types.InlineKeyboardMarkup()  # Разметка для кнопки уже в самой ленте сообщений
        xaker = types.InlineKeyboardButton('XakeR Python', url="https://xakep.ru/issues/xb/006/") #Кнопка в ленте
        markup.add(xaker)
        await bot.send_message(message.chat.id, 'Кликай!', reply_markup=markup)

    elif 'как дела' in message.text.lower():  # На вопрос...
        markup = types.InlineKeyboardMarkup(row_width=2)  # Два ответа
        good = types.InlineKeyboardButton('Отлично', callback_data='good')  # Первый
        bad = types.InlineKeyboardButton('Плохо', callback_data='bad')  # Второй
        markup.add(good, bad)
        await bot.send_message(message.chat.id, 'Хорошо,а у тебя?', parse_mode='html',reply_markup=markup)  # Отсылаем и ждём ответа (можно и не отвечать)

    elif 'игральная кость' in message.text.lower():  # Прикольный анимированный стикер с зариками
        await bot.send_dice(chat_id=message.chat.id)

    elif 'википедия' in message.text.lower(): #Поиск по Википедии
        await bot.send_message(message.chat.id,"Чтобы осуществить поиск по Википедия,введи запрос в формате:\n\n<b>WIKI: ЧТО НАДО НАЙТИ</b>",parse_mode='html')

    elif 'wiki:' in message.text.lower(): #Поис по Википедии (обработка запроса пользователя)
        letter_search = message.text.split(':')[-1] #Достаём само слово для поиска
        letter_search = letter_search.replace(" ","") #Убираем лишние пробелы,если есть
        await bot.send_message(message.chat.id,f"<b><i>{letter_search}</i></b>\n\n{wiki(letter_search)}",parse_mode='html') #Закидываем в функцию поиска и выводим

    elif message.text.lower() == '🛑 stop':  # На stop вызываем функцию остановки,либо пропишем /stop и она так же сработает напрямую
        await stopp(message.text)

    else:
        await bot.send_message(message.chat.id, message.text)  # Если просто так пишет,то отвечаем тем же(эхо-бот)

#Запускаем цикл работы бота с skip updates,для того чтобы когда бот не онлайн ему не слали смс
executor.start_polling(dp,skip_updates=True)

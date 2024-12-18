import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


bot = telebot.TeleBot("7686380954:AAFyuxX2Vx7diqpF-bM5HV133z5rGe214sA")


user_states = {}


@bot.message_handler(commands=['start'])
def handle_start(message):
    # Тут просят соглашение

    user_states[message.chat.id] = 'start'
    # менюшка соглашения
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True)
    button1 = KeyboardButton('да')
    button2 = KeyboardButton('нет')
    keyboard.add(button1, button2)

    bot.reply_to(message, 'Привет! Я бот. Ты принимаешь соглашение?',
                 reply_markup=keyboard)


@bot.message_handler(func=lambda message: user_states.get(
        message.chat.id) == 'start')
def handle_accept(message):
    # обработчик соглашения

    # удалятся клавиатура
    remove_keyboard = ReplyKeyboardRemove()

    # клавиатура для начального выбора
    keyboard = ReplyKeyboardMarkup()
    button1 = KeyboardButton('запись через салон')
    button2 = KeyboardButton('запись через мастера')
    button3 = KeyboardButton('просто дайте мне номер телефона')
    keyboard.add(button1, button2, button3)

    if message.text == "да":
        user_states[message.chat.id] = 'main_state'
        bot.reply_to(message, 'Соглашение одобрено, как хочешь записаться?',
                     reply_markup=keyboard)

    # если нет, то клавиатура удаляется, ничего не доступно
    elif message.text == "нет":
        user_states[message.chat.id] = 'declined'
        bot.reply_to(message, 'Вы отклонили соглашение',
                     reply_markup=remove_keyboard)


@bot.message_handler(func=lambda message: user_states.get(
        message.chat.id) == 'main_state')
def handle_main_state(message):
    # начальный этап

    if message.text == "запись через салон":
        # клавиатура салонов, надо соеденить с моделью салонов
        keyboard1 = ReplyKeyboardMarkup()

        button1 = KeyboardButton('салон 123')
        button2 = KeyboardButton('салон 321')
        button3 = KeyboardButton('салон 222')

        keyboard1.add(button1, button2, button3)

        user_states[message.chat.id] = 'salon'
        bot.reply_to(message, 'выбери салон', reply_markup=keyboard1)

    elif message.text == "запись через мастера":
        # клавиатура процедур, тоже соеденить с бэком
        inline_keyboard = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton("процедура 1",
                                       callback_data="procedure_1")
        button2 = InlineKeyboardButton("процедура 2",
                                       callback_data="procedure_2")
        button3 = InlineKeyboardButton("процедура 3",
                                       callback_data="procedure_3")

        inline_keyboard.add(button1, button2, button3)

        user_states[message.chat.id] = 'salon_master'
        bot.reply_to(message, 'выбери процедуру', reply_markup=inline_keyboard)

    elif message.text == "просто дайте мне номер телефона":
        # просто возврат в начальный этап
        keyboard = ReplyKeyboardMarkup()

        button1 = KeyboardButton('запись через салон')
        button2 = KeyboardButton('запись через мастера')
        button3 = KeyboardButton('просто дайте мне номер телефона')

        keyboard.add(button1, button2, button3)

        user_states[message.chat.id] = 'main_state'
        bot.reply_to(message, 'держи', reply_markup=keyboard)


@bot.message_handler(func=lambda message: user_states.get(
        message.chat.id) == 'salon')
def handle_salon(message):
    # выполняется, если мы выбрали 1 вариант: через салон, а затем выбрали салон

    # логику выбора надо будет поменять
    if message.text in ['салон 222', 'салон 321', 'салон 123']:
        user_states[message.chat.id] = 'salon_date'
        remove_keyboard = ReplyKeyboardRemove()

        # та же клавиатура процедур, должна быть привязана к выбранному салону
        inline_keyboard = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton("процедура 1",
                                       callback_data="procedure_1")
        button2 = InlineKeyboardButton("процедура 2",
                                       callback_data="procedure_2")
        button3 = InlineKeyboardButton("процедура 3",
                                       callback_data="procedure_3")
        inline_keyboard.add(button1, button2, button3)

        bot.send_message(message.chat.id, 'выбери процедуру',
                         reply_markup=remove_keyboard)
        bot.send_message(message.chat.id, 'процедуры',
                         reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda call: user_states.get(
        call.message.chat.id) == 'salon_date')
def handle_salon_date(call):
    # выполняется после выбора процедуры в варианте 1
    # логику выбора процедур надо будет так же поменять

    if call.data in ["procedure_1", 'procedure_2', 'procedure_3']:
        inline_keyboard = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("01.01",
                                       callback_data="date_1")
        button2 = InlineKeyboardButton("02.01",
                                       callback_data="date_2")
        button3 = InlineKeyboardButton("03.01",
                                       callback_data="date_3")
        inline_keyboard.add(button1, button2, button3)
        bot.send_message(call.message.chat.id, "процедура выбрана \n"
                         'выбери дату',
                         reply_markup=inline_keyboard)
        user_states[call.message.chat.id] = 'salon_time'


@bot.callback_query_handler(func=lambda call: user_states.get(
        call.message.chat.id) == 'salon_time')
def handle_salon_time(call):
    # выполняется после выбора даты

    if call.data in ['date_1', 'date_2', 'date_3']:

        # клавиатура выбора времени должна создаваться с помощью моделей

        inline_keyboard = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton("14:00",
                                       callback_data="time_1")
        button2 = InlineKeyboardButton("13:00",
                                       callback_data="time_2")
        button3 = InlineKeyboardButton("12:00",
                                       callback_data="time_3")
        inline_keyboard.add(button1, button2, button3)

        user_states[call.message.chat.id] = 'salon_phone'
        bot.send_message(call.message.chat.id, 'дата выбрана, выбери время',
                         reply_markup=inline_keyboard)


@bot.callback_query_handler(func=lambda call: user_states.get(
        call.message.chat.id) == 'salon_phone')
def handle_salon_phone(call):

    # выполняется после выбора времени

    if call.data in ['time_1', 'time_2', 'time_3']:
        bot.send_message(call.message.chat.id, 'Напишите номер телефона')
        user_states[call.message.chat.id] = 'salon_success'


@bot.message_handler(func=lambda message: user_states.get(
        message.chat.id) == 'salon_success')
def handle_phone_number(message):
    # клавиатура начального экрана
    keyboard = ReplyKeyboardMarkup()

    button1 = KeyboardButton('запись через салон')
    button2 = KeyboardButton('запись через мастера')
    button3 = KeyboardButton('просто дайте мне номер телефона')

    keyboard.add(button1, button2, button3)

    phone_number = message.text
    # phone_number, как я понял, надо добваить в бд
    # и не только phone_number нужно сохранять все данные в бд
    # должна быть модель записи
    user_states[message.chat.id] = 'main_state'
    bot.send_message(message.chat.id, 'Номер записан, возврат к началу',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: user_states.get(
        call.message.chat.id) == 'salon_master')
def handle_master(call):
    # Выполняется после выбора процедуры в варианте 2
    if call.data in ["procedure_1", 'procedure_2', 'procedure_3']:
        # клавиатура мастеров на эти процедуры, надо соеденять с бэком
        inline_keyboard = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton("Адольф",
                                       callback_data="master_1")
        button2 = InlineKeyboardButton("Никита",
                                       callback_data="master_2")
        button3 = InlineKeyboardButton("Марина",
                                       callback_data="master_3")
        inline_keyboard.add(button1, button2, button3)

        bot.send_message(call.message.chat.id, 'выбери мастера',
                         reply_markup=inline_keyboard)
        user_states[call.message.chat.id] = 'master_date'


@bot.callback_query_handler(func=lambda call: user_states.get(
        call.message.chat.id) == 'master_date')
def handle_master_date(call):
    # выполняется после выбора мастера
    if call.data in ["master_1", 'master_2', 'master_3']:
        # клавиатура выбора дат, должно быть связано с бэком
        inline_keyboard = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton("01.01",
                                       callback_data="date_1")
        button2 = InlineKeyboardButton("02.01",
                                       callback_data="date_2")
        button3 = InlineKeyboardButton("03.01",
                                       callback_data="date_3")
        inline_keyboard.add(button1, button2, button3)

        bot.send_message(call.message.chat.id, 'выбери дату',
                         reply_markup=inline_keyboard)
        user_states[call.message.chat.id] = 'master_time'


@bot.callback_query_handler(func=lambda call: user_states.get(
        call.message.chat.id) == 'master_time')
def handle_master_time(call):
    # выполняется после выбора даты
    if call.data in ["date_1", 'date_2', 'date_3']:
        # клавиатура выбора времени, должно быть связано с бэком
        inline_keyboard = InlineKeyboardMarkup()

        button1 = InlineKeyboardButton("12:00",
                                       callback_data="time_1")
        button2 = InlineKeyboardButton("13:00",
                                       callback_data="time_2")
        button3 = InlineKeyboardButton("14:00",
                                       callback_data="time_3")
        inline_keyboard.add(button1, button2, button3)
        bot.send_message(call.message.chat.id, 'выбери время',
                         reply_markup=inline_keyboard)
        user_states[call.message.chat.id] = 'master_success'


@bot.callback_query_handler(func=lambda call: user_states.get(
        call.message.chat.id) == 'master_success')
def handle_master_success(call):
    # выполняется после выбора времени
    if call.data in ["time_1", 'time_2', 'time_3']:
        # просто начальная клавиатура
        keyboard = ReplyKeyboardMarkup()
        button1 = KeyboardButton('запись через салон')
        button2 = KeyboardButton('запись через мастера')
        button3 = KeyboardButton('просто дайте мне номер телефона')
        keyboard.add(button1, button2, button3)

        bot.send_message(call.message.chat.id, 'вы записаны, ваш салон',
                         reply_markup=keyboard)
        user_states[call.message.chat.id] = 'main_state'


if __name__ == "__main__":
    bot.polling()


# это просто интерфейс и логика в нём немного глупая
# нужно будет доделать клавиатуры, чтобы они отображали актуальные данные
# нужно будет сделать нормальное сохранение данных в бд

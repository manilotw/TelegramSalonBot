import os
import django
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from django.conf import settings

# Убедитесь, что Django настроен
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_city.settings')  # Укажите путь к вашему settings.py
django.setup()

from beauty_bot.models import Services, Specialist, Clients, TimeSlot, Schedule  # Импорт моделей

bot = TeleBot("7686380954:AAFyuxX2Vx7diqpF-bM5HV133z5rGe214sA")  # Замените на ваш API ключ

user_states = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_states[message.chat.id] = 'start'
    keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)  # уменьшены кнопки
    button1 = KeyboardButton('да')
    button2 = KeyboardButton('нет')
    keyboard.add(button1, button2)

    bot.reply_to(message, 'Привет! Ты принимаешь соглашение?', reply_markup=keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'start')
def handle_accept(message):
    remove_keyboard = ReplyKeyboardRemove()

    if message.text == "да":
        user_states[message.chat.id] = 'main_state'
        services = Services.objects.all()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # уменьшены кнопки
        for service in services:
            keyboard.add(KeyboardButton(service.name))
        bot.reply_to(message, 'Выберите услугу:', reply_markup=keyboard)

    elif message.text == "нет":
        user_states[message.chat.id] = 'declined'
        bot.reply_to(message, 'Вы отклонили соглашение', reply_markup=remove_keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'main_state')
def handle_service_selection(message):
    service_name = message.text
    service = Services.objects.filter(name=service_name).first()

    if service:
        user_states[message.chat.id] = 'select_specialist'
        specialists = Specialist.objects.filter(service=service)
        inline_keyboard = InlineKeyboardMarkup()
        for specialist in specialists:
            inline_keyboard.add(InlineKeyboardButton(specialist.name, callback_data=specialist.name))
        bot.send_message(message.chat.id, 'Выберите специалиста:', reply_markup=inline_keyboard)
    else:
        bot.reply_to(message, 'Такой услуги нет. Попробуйте снова.')

@bot.callback_query_handler(func=lambda call: user_states.get(call.message.chat.id) == 'select_specialist')
def handle_specialist_selection(call):
    specialist_name = call.data
    specialist = Specialist.objects.filter(name=specialist_name).first()

    if specialist:
        user_states[call.message.chat.id] = 'select_time'
        time_slots = TimeSlot.objects.filter(specialist=specialist, is_booked=False)
        inline_keyboard = InlineKeyboardMarkup()
        for time_slot in time_slots:
            inline_keyboard.add(InlineKeyboardButton(f'{time_slot.date} {time_slot.time}', callback_data=f'{time_slot.id}'))
        bot.send_message(call.message.chat.id, 'Выберите время:', reply_markup=inline_keyboard)
    else:
        bot.send_message(call.message.chat.id, 'Такого мастера нет. Выберите другого мастера:')
        # Повторить выбор мастера
        service_name = user_states.get(call.message.chat.id, {}).get('service_name', '')
        service = Services.objects.filter(name=service_name).first()
        if service:
            specialists = Specialist.objects.filter(service=service)
            inline_keyboard = InlineKeyboardMarkup()
            for specialist in specialists:
                inline_keyboard.add(InlineKeyboardButton(specialist.name, callback_data=specialist.name))
            bot.send_message(call.message.chat.id, 'Выберите специалиста:', reply_markup=inline_keyboard)

@bot.callback_query_handler(func=lambda call: user_states.get(call.message.chat.id) == 'select_time')
def handle_time_slot_selection(call):
    time_slot_id = call.data
    time_slot = TimeSlot.objects.filter(id=time_slot_id).first()

    if time_slot:
        user_states[call.message.chat.id] = 'enter_phone'
        bot.send_message(call.message.chat.id, 'Введите ваш номер телефона:') 

        # Сохраняем информацию о временном слоте
        user_states[call.message.chat.id] = {
            'time_slot': time_slot,
            'specialist': time_slot.specialist,
            'service': time_slot.specialist.service.first()
        }
    else:
        bot.send_message(call.message.chat.id, 'Такого времени нет. Выберите другое время:')
        # Предложить выбрать время заново
        specialist_name = user_states.get(call.message.chat.id, {}).get('specialist_name', '')
        specialist = Specialist.objects.filter(name=specialist_name).first()
        if specialist:
            time_slots = TimeSlot.objects.filter(specialist=specialist, is_booked=False)
            inline_keyboard = InlineKeyboardMarkup()
            for time_slot in time_slots:
                inline_keyboard.add(InlineKeyboardButton(f'{time_slot.date} {time_slot.time}', callback_data=f'{time_slot.id}'))
            bot.send_message(call.message.chat.id, 'Выберите время:', reply_markup=inline_keyboard)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'enter_phone')
def handle_phone_number(message):
    phone_number = message.text
    user_data = user_states[message.chat.id]
    time_slot = user_data.get('time_slot')
    specialist = user_data.get('specialist')
    service = user_data.get('service')

    if not time_slot or not specialist or not service:
        bot.send_message(message.chat.id, 'Ошибка! Пожалуйста, попробуйте заново.')
        return

    client = Clients(name=message.from_user.first_name,
                     telegram_username=message.from_user.username,
                     phone_number=phone_number)
    client.save()

    # Бронирование
    schedule = Schedule(client=client,
                        specialist=specialist,
                        service=service,
                        time_slot=time_slot)
    schedule.save()

    # Обновляем временной слот как занятый
    time_slot.is_booked = True
    time_slot.save()

    bot.send_message(message.chat.id, f'Ваше бронирование на услугу "{service.name}" с мастером {specialist.name} на {time_slot.date} в {time_slot.time} подтверждено!')

    # Завершаем процесс
    user_states[message.chat.id] = 'main_state'
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # уменьшены кнопки
    button1 = KeyboardButton('запись через салон')
    button2 = KeyboardButton('запись через мастера')
    button3 = KeyboardButton('просто дайте мне номер телефона')
    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, 'Запись завершена, возврат в меню', reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling()

print("Loading...")
from django.core.management.base import BaseCommand

import os
import django
from django.core.paginator import Paginator
from django.core.checks import messages
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "urfon.settings")
# django.setup()
import json

from django.shortcuts import get_object_or_404
import telebot
from telebot import types
from app.models import *
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage
state_storage = StateMemoryStorage()

TOKEN = "5059478535:AAEVb7Vz1Jh7TdRg0EE89dNn-RYAPaDgZKo"
chat_id = '-1001594110730'

i_start = """👋Assalomu alaykum
Urfon ta`lim rasmiy 🤖botiga xush kelibsiz
Bu bot orqali siz bizning imtixonlarimizga online tarzda ro`yxatdan o`tishingiz mumkin‼️

Bu botdan foydalanish uchun bizning kanalimizga a`zo bo`lishingizni so`rab qolamiz. Chunki javoblar bizning rasmiy kanalimizda e`lon qilinadi.
"""


bot = telebot.TeleBot(TOKEN, parse_mode='html')

class MyStates(StatesGroup):
    start = State()
    menu = State()
    fanlar = State()
    get_contact = State()
    fio = State()
    subcategory = State()
    product = State()
    buying = State()
    buy_sum = State()
    conforming = State()
    complate = State()

def s_dataW(fkey_, value_, v_ = False):
    sts = Profile.objects.get(tid=fkey_)
    
    if v_:
        sts.state = str(value_).split(":")[1] + "^" + str(v_)
    else:
        sts.state = str(value_).split(":")[1]
    bot.set_state(fkey_, value_, fkey_)
    sts.save()

for i in Profile.objects.all():
    bot.set_state(i.tid, getattr(MyStates, i.state.split("^")[0]), i.tid)

def excel():
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    for i in Order.objects.all():
        ws.append([str(i.id), i.name, str(i.science), i.created_time, i.user.phone])
    wb.save('output.xlsx')

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Obuna bo`lish", url='https://t.me/eduabgroup'),
                               InlineKeyboardButton("Tekshirish", callback_data="reflash"))
    return markup

def fanlarf():
    markup = types.ReplyKeyboardMarkup()
    markup.row_width = 2
    argv = []
    for i in Science.objects.all():
        argv.append(types.KeyboardButton(i.title))
    argv.append(types.KeyboardButton("Orqaga"))
    markup.add(*argv)
    return markup


def menuf():
    menu_ = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Imtihonga ro`yxatdan o`tish')
    itembtn2 = types.KeyboardButton('Biz bilan aloqa')
    menu_.row(itembtn1)
    menu_.row(itembtn2)
    return menu_

def back_to():

    menu_ = types.ReplyKeyboardMarkup()
    menu_.resize_keyboard = True
    itembtn2 = types.KeyboardButton('Orqaga')
    menu_.row(itembtn2)
    return menu_


@bot.message_handler(commands=['start'])
def starting(message):
    if message.chat.type == "supergroup" or message.chat.type == "group":
        bot.send_message(message.chat.id, "Bot ishlamoqda")
    else:
        user = Profile.objects.filter(tid = message.chat.id)
        if not user or not user[0].phone:
            keyboard = types.ReplyKeyboardMarkup()
            reg_button = types.KeyboardButton(text="📞 Telefon raqamingizni yuboring ", request_contact=True)
            keyboard.add(reg_button)
            bot.send_message(message.chat.id, i_start, reply_markup=keyboard)
            if not user:
                Profile.objects.create(tid=message.chat.id).save()
            s_dataW(message.chat.id, MyStates.get_contact)
        else:
            bot.send_message(message.chat.id, "Siz allaqachon ro`yxatdan o`tgansiz!!!", reply_markup=menuf())
            s_dataW(message.chat.id, MyStates.menu)

@bot.message_handler(state=MyStates.get_contact, content_types=['contact'])
def get_contact(message):
    user = Profile.objects.get(tid = message.chat.id)
    number = message.contact.phone_number
    user.phone = number.replace("+", "")
    user.save()
    bot.send_message(message.chat.id,"Telefon raqamingiz saqlandi.", reply_markup=ReplyKeyboardRemove())
    print(bot.get_chat_member(chat_id,message.from_user.id))
    if bot.get_chat_member(chat_id,message.from_user.id).status in ['administrator','creator', 'member']:
        bot.send_message(message.chat.id, "Bizning bo`timizdan Urfon ta`lim markazimizda imtihon topshirish uchun foydalana olasiz!!!", reply_markup=menuf())
        s_dataW(message.chat.id, MyStates.menu)
    else:
        bot.send_message(message.chat.id, 'Bu botdan foydalanish uchun bizning kanalimizga obuna bo`lishingiz kerak', reply_markup=gen_markup())

@bot.message_handler(state=MyStates.menu)
def menu(message):
    #user = Profile.objects.get(tid = message.chat.id)
    if message.text == 'Imtihonga ro`yxatdan o`tish':
        bot.send_message(message.chat.id, "Topshirmoqchi bo`lgan Faningizni tanlang", reply_markup=fanlarf())
        s_dataW(message.chat.id, MyStates.fanlar)
    elif message.text == 'Biz bilan aloqa':
        bot.send_message(message.chat.id, "Aloqa uchun:\nTel: +998999999999\nTelegram: @bunyodbekab")
    elif message.text == 'excel':
        bot.send_message(message.chat.id, "Sabr...")
        excel()
        fl = open("output.xlsx", 'rb')
        bot.send_document(chat_id=message.chat.id, document=fl)
        

@bot.message_handler(state=MyStates.fanlar)
def fanlar(message):
    #user = Profile.objects.get(tid = message.chat.id)
    obj = Science.objects.filter(title=message.text)
    if obj:
        bot.send_message(message.chat.id, f"{obj[0].title} fanidan imtihonda qatnashish uchun ism familiyangizni yuboring!!!", reply_markup=back_to())
        s_dataW(message.chat.id, MyStates.fio, v_ = obj[0].id)
    elif message.text == 'Orqaga':
        bot.send_message(message.chat.id, "Menyu", reply_markup=menuf())
        s_dataW(message.chat.id, MyStates.menu)



@bot.message_handler(state=MyStates.fio)
def fio(message):
    user = Profile.objects.get(tid = message.chat.id)
    obj = Science.objects.get(id = user.state.split("^")[1])
    if message.text == 'Orqaga':
        bot.send_message(message.chat.id, "Menyu", reply_markup=menuf())
        s_dataW(message.chat.id, MyStates.menu)
    else:
        names = message.text
        Order.objects.create(user=user, science=obj, name=names).save()
        bot.send_message(message.chat.id, "Siz muvoffaqiyatli ro`yxatdan o`tdingiz", reply_markup=menuf())
        s_dataW(message.chat.id, MyStates.menu)
        bot.send_message(message.chat.id, f"Ism: {names}\nTelefon: {user.phone}\nFani: {obj.title}")




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "reflash":
        if bot.get_chat_member(chat_id,message.from_user.id).status in ['administrator','creator', 'member']:
            bot.send_message(call.from_user.id, "Bizning bo`timizdan Urfon ta`lim markazimizda imtihon topshirish uchun foydalan olasiz!!!", reply_markup=menuf())
            s_dataW(message.chat.id, MyStates.menu)

bot.add_custom_filter(custom_filters.StateFilter(bot))

def heading():
    bot.polling()
print('Started')
#heading()
print("End")
def polToWebhook(request):
    update = telebot.types.Update.de_json(json.loads(request.body.decode('utf-8')))
    bot.process_new_updates([update])
    return True
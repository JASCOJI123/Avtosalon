from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
def menu():
 return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="🚘 Avtomobillar"),KeyboardButton(text="💳 Kredit")],[KeyboardButton(text="📅 Test-drive"),KeyboardButton(text="🔥 Aksiyalar")],[KeyboardButton(text="📞 Menejer bilan bog‘lanish")]],resize_keyboard=True)
def phone():
 return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="📱 Telefon raqamimni yuborish",request_contact=True)]],resize_keyboard=True,one_time_keyboard=True)
def cars(items):
 return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"{x.brand} {x.model} — {x.price:,} so‘m",callback_data=f"car:{x.id}")] for x in items])

from aiogram import Bot,Dispatcher,F
from aiogram.filters import CommandStart
from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message,CallbackQuery
from sqlalchemy import select
from .config import settings
from .db import SessionLocal
from .models import Vehicle,Lead,TestDrive,Promotion
from .keyboards import menu,phone,cars
bot=Bot(settings.bot_token); dp=Dispatcher()
class LeadFlow(StatesGroup): phone=State()
class TestFlow(StatesGroup): name=State(); phone=State(); time=State()
@dp.message(CommandStart())
async def start(m:Message): await m.answer("🚘 <b>AutoSalon</b>\nAvtomobil tanlang yoki test-drive buyurtma qiling.",parse_mode="HTML",reply_markup=menu())
@dp.message(F.text=="🚘 Avtomobillar")
async def catalog(m:Message):
 async with SessionLocal() as db:
  r=await db.execute(select(Vehicle).where(Vehicle.active==True).order_by(Vehicle.brand,Vehicle.model)); xs=r.scalars().all()
 await m.answer("🚘 Avtomobilni tanlang:",reply_markup=cars(xs)) if xs else await m.answer("Katalog bo‘sh.")
@dp.callback_query(F.data.startswith("car:"))
async def detail(c:CallbackQuery,state:FSMContext):
 async with SessionLocal() as db: v=await db.get(Vehicle,int(c.data.split(":")[1]))
 if not v: await c.answer("Topilmadi",show_alert=True); return
 await state.update_data(vehicle_id=v.id); txt=f"🚘 <b>{v.brand} {v.model}</b>\n📅 {v.year}\n💰 {v.price:,} so‘m\n\n{v.description}\n\n📞 Qiziqsangiz telefon yuboring."
 if v.photo_url: await c.message.answer_photo(v.photo_url,caption=txt,parse_mode="HTML",reply_markup=phone())
 else: await c.message.answer(txt,parse_mode="HTML",reply_markup=phone())
 await state.set_state(LeadFlow.phone); await c.answer()
@dp.message(LeadFlow.phone,F.contact)
async def save_lead(m:Message,state:FSMContext):
 d=await state.get_data()
 async with SessionLocal() as db: db.add(Lead(telegram_id=m.from_user.id,name=m.from_user.full_name,phone=m.contact.phone_number,vehicle_id=d.get("vehicle_id"))); await db.commit()
 await notify(f"🆕 <b>Yangi lead</b>\n👤 {m.from_user.full_name}\n📞 {m.contact.phone_number}\n🚘 ID: {d.get('vehicle_id')}")
 await m.answer("✅ Qabul qilindi. Menejer bog‘lanadi.",reply_markup=menu()); await state.clear()
@dp.message(F.text=="📞 Menejer bilan bog‘lanish")
async def manager(m:Message,state:FSMContext): await m.answer("📱 Telefon raqamingizni yuboring:",reply_markup=phone()); await state.set_state(LeadFlow.phone)
@dp.message(F.text=="📅 Test-drive")
async def td(m:Message,state:FSMContext): await m.answer("👤 Ismingiz:"); await state.set_state(TestFlow.name)
@dp.message(TestFlow.name)
async def td_name(m:Message,state:FSMContext): await state.update_data(name=m.text); await m.answer("📱 Telefon:",reply_markup=phone()); await state.set_state(TestFlow.phone)
@dp.message(TestFlow.phone,F.contact)
async def td_phone(m:Message,state:FSMContext): await state.update_data(phone=m.contact.phone_number); await m.answer("🕐 Qulay sana va vaqt?"); await state.set_state(TestFlow.time)
@dp.message(TestFlow.time)
async def td_time(m:Message,state:FSMContext):
 d=await state.get_data()
 async with SessionLocal() as db: db.add(TestDrive(telegram_id=m.from_user.id,name=d["name"],phone=d["phone"],preferred_time=m.text)); await db.commit()
 await notify(f"📅 <b>Test-drive</b>\n👤 {d['name']}\n📞 {d['phone']}\n🕐 {m.text}"); await m.answer("✅ Test-drive so‘rovi qabul qilindi.",reply_markup=menu()); await state.clear()
@dp.message(F.text=="💳 Kredit")
async def credit(m:Message): await m.answer("💳 Kredit kalkulyatori Web App'da mavjud.")
@dp.message(F.text=="🔥 Aksiyalar")
async def promos(m:Message):
 async with SessionLocal() as db: r=await db.execute(select(Promotion).where(Promotion.active==True).order_by(Promotion.created_at.desc())); xs=r.scalars().all()
 await m.answer("\n\n".join(f"🔥 <b>{x.title}</b>\n{x.text}" for x in xs),parse_mode="HTML") if xs else await m.answer("Aksiya yo‘q.")
async def notify(text):
 for aid in settings.admins:
  try: await bot.send_message(aid,text,parse_mode="HTML")
  except Exception: pass

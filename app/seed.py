import asyncio
from .db import SessionLocal
from .models import Vehicle,Promotion
from sqlalchemy import select
async def main():
 async with SessionLocal() as db:
  if not (await db.execute(select(Vehicle))).scalars().first():
   db.add_all([Vehicle(brand="Chevrolet",model="Cobalt",price=125000000,year=2026,description="Ommabop sedan."),Vehicle(brand="BYD",model="Song Plus",price=320000000,year=2026,description="Gibrid crossover."),Vehicle(brand="Kia",model="K5",price=390000000,year=2026,description="Biznes sedan.")])
  if not (await db.execute(select(Promotion))).scalars().first(): db.add(Promotion(title="Maxsus taklif",text="Tanlangan avtomobillarga maxsus shartlar."))
  await db.commit()
if __name__=="__main__": asyncio.run(main())

from datetime import datetime
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
from sqlalchemy import String,BigInteger,Integer,Boolean,Text,DateTime,ForeignKey
class Base(DeclarativeBase): pass
class Vehicle(Base):
    __tablename__="vehicles"; id:Mapped[int]=mapped_column(primary_key=True)
    brand:Mapped[str]=mapped_column(String(80),index=True); model:Mapped[str]=mapped_column(String(120),index=True)
    price:Mapped[int]=mapped_column(BigInteger); year:Mapped[int]=mapped_column(Integer)
    description:Mapped[str]=mapped_column(Text,default=""); photo_url:Mapped[str|None]=mapped_column(String(1000),nullable=True)
    active:Mapped[bool]=mapped_column(Boolean,default=True)
class Manager(Base):
    __tablename__="managers"; id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(160)); telegram_id:Mapped[int|None]=mapped_column(BigInteger,nullable=True)
    active:Mapped[bool]=mapped_column(Boolean,default=True)
class Lead(Base):
    __tablename__="leads"; id:Mapped[int]=mapped_column(primary_key=True)
    telegram_id:Mapped[int]=mapped_column(BigInteger,index=True); name:Mapped[str]=mapped_column(String(160))
    phone:Mapped[str]=mapped_column(String(40)); vehicle_id:Mapped[int|None]=mapped_column(ForeignKey("vehicles.id"))
    manager_id:Mapped[int|None]=mapped_column(ForeignKey("managers.id")); source:Mapped[str]=mapped_column(String(40),default="telegram")
    status:Mapped[str]=mapped_column(String(40),default="new"); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class TestDrive(Base):
    __tablename__="test_drives"; id:Mapped[int]=mapped_column(primary_key=True)
    telegram_id:Mapped[int]=mapped_column(BigInteger); name:Mapped[str]=mapped_column(String(160)); phone:Mapped[str]=mapped_column(String(40))
    vehicle_id:Mapped[int|None]=mapped_column(ForeignKey("vehicles.id")); preferred_time:Mapped[str]=mapped_column(String(100))
    status:Mapped[str]=mapped_column(String(40),default="new"); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Promotion(Base):
    __tablename__="promotions"; id:Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]=mapped_column(String(200)); text:Mapped[str]=mapped_column(Text)
    active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

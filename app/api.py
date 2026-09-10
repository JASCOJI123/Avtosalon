from fastapi import APIRouter,Depends,HTTPException,Request,Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from itsdangerous import URLSafeTimedSerializer,BadSignature
from .config import settings
from .db import get_db
from .models import Vehicle,Lead,TestDrive,Promotion
from pydantic import BaseModel
router=APIRouter(); ser=URLSafeTimedSerializer(settings.secret_key)
class VehicleIn(BaseModel): brand:str; model:str; price:int; year:int=2026; description:str=""; photo_url:str|None=None; active:bool=True
class PromoIn(BaseModel): title:str; text:str; active:bool=True
def admin(request:Request):
 token=request.cookies.get("admin_session")
 if not token: raise HTTPException(401,"Login required")
 try: return ser.loads(token,max_age=86400)
 except BadSignature: raise HTTPException(401,"Login expired")
@router.get("/vehicles")
async def public_cars(db:AsyncSession=Depends(get_db)):
 r=await db.execute(select(Vehicle).where(Vehicle.active==True).order_by(Vehicle.brand,Vehicle.model)); return [{"id":x.id,"brand":x.brand,"model":x.model,"price":x.price,"year":x.year,"description":x.description,"photo_url":x.photo_url} for x in r.scalars().all()]
@router.get("/promotions")
async def public_promos(db=Depends(get_db)):
 r=await db.execute(select(Promotion).where(Promotion.active==True)); return [{"id":x.id,"title":x.title,"text":x.text} for x in r.scalars().all()]
@router.post("/admin/login")
async def login(username:str=Form(...),password:str=Form(...)):
 if username!=settings.admin_username or password!=settings.admin_password: raise HTTPException(401,"Invalid credentials")
 resp=JSONResponse({"ok":True}); resp.set_cookie("admin_session",ser.dumps({"u":username}),httponly=True,samesite="lax",secure=False,max_age=86400); return resp
@router.post("/admin/logout")
async def logout(request:Request): admin(request); r=JSONResponse({"ok":True}); r.delete_cookie("admin_session"); return r
@router.get("/admin/stats")
async def stats(request:Request,db=Depends(get_db)):
 admin(request); return {"leads":(await db.execute(select(func.count(Lead.id)))).scalar() or 0,"test_drives":(await db.execute(select(func.count(TestDrive.id)))).scalar() or 0,"vehicles":(await db.execute(select(func.count(Vehicle.id)).where(Vehicle.active==True))).scalar() or 0}
@router.get("/admin/leads")
async def leads(request:Request,db=Depends(get_db)):
 admin(request); r=await db.execute(select(Lead).order_by(Lead.created_at.desc()).limit(500)); return [{"id":x.id,"name":x.name,"phone":x.phone,"vehicle_id":x.vehicle_id,"status":x.status,"created_at":x.created_at.isoformat()} for x in r.scalars().all()]
@router.patch("/admin/leads/{lead_id}")
async def lead_status(lead_id:int,status:str,request:Request,db=Depends(get_db)):
 admin(request); x=await db.get(Lead,lead_id)
 if not x: raise HTTPException(404,"Lead not found")
 if status not in {"new","contacted","test_drive","sold","lost"}: raise HTTPException(400,"Invalid status")
 x.status=status; await db.commit(); return {"ok":True}
@router.post("/admin/vehicles")
async def add_vehicle(data:VehicleIn,request:Request,db=Depends(get_db)):
 admin(request); x=Vehicle(**data.model_dump()); db.add(x); await db.commit(); await db.refresh(x); return {"id":x.id}
@router.delete("/admin/vehicles/{vehicle_id}")
async def del_vehicle(vehicle_id:int,request:Request,db=Depends(get_db)):
 admin(request); x=await db.get(Vehicle,vehicle_id)
 if not x: raise HTTPException(404,"Not found")
 x.active=False; await db.commit(); return {"ok":True}
@router.post("/admin/promotions")
async def add_promo(data:PromoIn,request:Request,db=Depends(get_db)):
 admin(request); x=Promotion(**data.model_dump()); db.add(x); await db.commit(); await db.refresh(x); return {"id":x.id}

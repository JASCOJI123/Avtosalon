import asyncio
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from .config import settings
from .bot import bot,dp
from .api import router
@asynccontextmanager
async def lifespan(app):
 task=asyncio.create_task(dp.start_polling(bot)); yield; task.cancel(); await bot.session.close()
app=FastAPI(title="AutoSalon Pro",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.cors or ["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router,prefix="/api")
app.mount("/static",StaticFiles(directory="web"),name="static")
@app.get("/")
async def home(): return FileResponse("web/index.html")
@app.get("/admin")
async def admin_page(): return FileResponse("web/admin.html")
@app.get("/health")
async def health(): return {"status":"ok"}
if __name__=="__main__": uvicorn.run("app.__main__:app",host="0.0.0.0",port=int(os.getenv("PORT","8000")))

from fastapi import FastAPI
from app.database import Base, engine
from app.auth.router import router as auth_router
from app.entries.router import router as entries_router
from app.tags.router import router as tags_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Dev Journal API")

app.include_router(auth_router)
app.include_router(entries_router)
app.include_router(tags_router)
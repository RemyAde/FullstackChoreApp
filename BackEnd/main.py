from fastapi import FastAPI
import models
from database import engine
from routers import auth, chores
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="../FrontEnd/static"), name="static")

app.include_router(auth.router)
app.include_router(chores.router)
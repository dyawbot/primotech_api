from fastapi import FastAPI
from config import engine

import model


model.Base.metadata.create_all(bind=engine)

app = FastAPI()



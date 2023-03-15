from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, client, instalation, inverter, module, project, user

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(auth.router)
app.include_router(client.router)
app.include_router(instalation.router)
app.include_router(inverter.router)
app.include_router(module.router)
app.include_router(project.router)
app.include_router(user.router)
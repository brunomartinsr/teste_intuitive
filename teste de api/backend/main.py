from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.rota_operadoras import router as operadoras  

app = FastAPI() #iniciando a aplicação

app.add_middleware(#configurando o CORS
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(operadoras)# Definição do router
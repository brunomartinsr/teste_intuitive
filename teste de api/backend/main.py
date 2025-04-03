import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.rota_operadoras import router as operadoras
from dotenv import load_dotenv

load_dotenv()  # Carrega variáveis de ambiente do .env

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(operadoras)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))

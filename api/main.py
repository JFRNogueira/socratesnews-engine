from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Criar a instância do FastAPI
app = FastAPI()

# Modelo de dados usando Pydantic
class Item(BaseModel):
    nome: str
    preco: float
    disponivel: bool = True

# Rota GET básica
@app.get("/")
def read_root():
    return {"mensagem": "Bem-vindo à API"}

# Rota GET com parâmetro
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Rota POST para criar um item
@app.post("/items/")
def create_item(item: Item):
    return item

# Para rodar o servidor
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
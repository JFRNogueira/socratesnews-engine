from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from journalist.rpa_search import RPASearch
from journalist.rpa_starter import RPAStart
from journalist.rpa_writer import RPAWriter

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
    return {"mensagem": "Ambiente de criação de APIs gerado com sucesso."}

# # Rota GET com parâmetro
# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}

# Rota POST para criar um item
@app.post("/create-news")
def create_news():
    sections = ['Mundo', 'Brasil', 'CeT', 'Economia', 'Entretenimento', 'Esporte']
    n_news_by_section = 6
    for s in sections:
        RPAStart(s, n_news_by_section)
    
    RPASearch()
    
    should_continue = True
    n_new_news = 0
    while should_continue:
        try:
            RPAWriter()
            n_new_news += 1
        except Exception as e:
            print('Erro ao criar notícia:', e)
            should_continue = False
    
    return {"n_new_news": n_new_news}


# Para rodar o servidor
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
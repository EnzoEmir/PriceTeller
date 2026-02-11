# Price Teller

<!-- Depois a gente melhora a descrição kkkkk -->
Este é um website sobre busca de preços interativa sobre listas de compras, com foco em componentes de componentes de computadores.

## Como rodar?

<!-- depois colocar aqui sobre como rodar. -->

### Para rodar o backend

###### Primeiro, inicie um ambiente virtual do python

```
cd backend
python -m venv .venv
```

###### Ative o ambiente virtual

```
.\venv\Scripts\Activate
```

###### Instale as depedências em seu ambiente virtual

```
pip install -r requirements.txt
```

###### Rode a aplicação com Uvicorn

```
uvicorn main:app --reload
```
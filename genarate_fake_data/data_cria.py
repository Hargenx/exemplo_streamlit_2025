import random
import pandas as pd

colunas = [
    "id_pedido",
    "id_produto",
    "id_loja",
    "nome_produto",
    "categoria_produto",
    "cidade",
    "data_venda",
    "quantidade_vendida",
    "valor_venda",
]

cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte"]
categorias = [
    "Ferramentas de Desenvolvimento",
    "Ferramentas Educacionais",
    "Ferramentas Criativas",
]
produtos = ["CodeCode", "HargenXtudio", "UI/UX-K", "PowerPro", "LostFost"]

def gerar_datas_aleatorias(n, start_date="2022-01-01", end_date="2024-12-31"):
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    return [start + (end - start) * random.random() for _ in range(n)]


data = {
    "id_pedido": range(1, 2000),
    "id_produto": [random.randint(10, 100) for _ in range(1999)],
    "id_loja": [random.randint(1, 5) for _ in range(1999)],
    "nome_produto": [random.choice(produtos) for _ in range(1999)],
    "categoria_produto": [random.choice(categorias) for _ in range(1999)],
    "cidade": [random.choice(cidades) for _ in range(1999)],
    "data_venda": gerar_datas_aleatorias(1999),
    "quantidade_vendida": [random.randint(1, 20) for _ in range(1999)],
    "valor_venda": [round(random.uniform(10, 500), 2) for _ in range(1999)],
}

# Formatar as datas para o formato brasileiro (dd/mm/yyyy)
data["data_venda"] = pd.to_datetime(data["data_venda"]).strftime("%d/%m/%Y")

df_new = pd.DataFrame(data, columns=colunas)
output_path = "./data/data.csv"
df_new.to_csv(output_path, index=False, encoding="utf-8")

output_path

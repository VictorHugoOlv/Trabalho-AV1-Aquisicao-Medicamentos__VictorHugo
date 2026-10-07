import pandas as pd

def money(v):
    return f'R$ {v:,.2f}'

def solution_table(df):
    out = df[['no_fornecedor','registros','preco_referencia','limite_fornecimento','quantidade_otima','custo_fornecedor','participacao']].copy()
    out.columns = ['Fornecedor','Registros','Preço referência','Limite','Quantidade ótima','Custo','Participação']
    return out

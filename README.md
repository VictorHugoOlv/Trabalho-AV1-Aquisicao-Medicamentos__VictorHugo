# 💊 Projeto 2 — Aquisição de Medicamentos

Sistema de Apoio à Tomada de Decisão (SAD) para distribuição ótima da aquisição de um medicamento entre fornecedores, usando Programação Linear e a base BPS 2025 fornecida no trabalho.

## Arquitetura

`BPS CSV → carregamento → tratamento → seleção do medicamento/fornecedores → parâmetros históricos → Programação Linear → solução ótima → análise de sensibilidade → recomendação → Streamlit`

- **Python + Pandas:** ingestão e tratamento dos dados.
- **SciPy / HiGHS:** resolução da Programação Linear.
- **Streamlit:** interface de decisão.
- **Matplotlib:** visualização dos resultados.
- **Pytest:** teste automatizado do modelo.

## Estrutura

```text
app.py
data/
  raw/aquisicoes-medicas-2025.csv
  processed/
src/
  data/loader.py
  data/preprocessing.py
  optimization/model.py
  optimization/solver.py
  analysis/sensitivity.py
  analysis/recommendation.py
  ui/components.py
tests/test_model.py
docs/modelo.md
outputs/
requirements.txt
```

## Como executar

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

Testes:

```bash
pytest
```

## Dados e critérios da primeira versão

O trabalho exige selecionar um único medicamento, mesma apresentação/unidade e pelo menos cinco fornecedores. Esta versão seleciona automaticamente o item com maior número de fornecedores que atende esse critério e, por padrão, usa os cinco fornecedores com maior quantidade de registros históricos para o item.

Para cada fornecedor:
- **Preço de referência:** mediana do preço unitário histórico.
- **Limite de fornecimento:** percentil 90% das quantidades históricas por fornecedor.
- **Demanda inicial:** 50% da soma dos limites dos fornecedores selecionados. O usuário pode alterá-la na interface.

Essas escolhas são parâmetros de modelagem da primeira versão e estão documentadas para que possam ser substituídas por critérios definidos pelo grupo/professor.

## Resultado de referência gerado pela primeira versão

Com os parâmetros padrão e os dados fornecidos, a execução seleciona **Enoxaparina 100 mg/mL, solução injetável, seringa preenchida**, unidade `SERINGA`. A demanda padrão é 217.806,75 unidades. O custo ótimo calculado é **R$ 1.716.317,19**, usando integralmente o limite necessário do fornecedor com menor preço de referência entre os cinco selecionados.

Os arquivos em `outputs/` registram a solução e a sensibilidade produzidas nessa execução. Para reproduzir:

```bash
python run_analysis.py
```

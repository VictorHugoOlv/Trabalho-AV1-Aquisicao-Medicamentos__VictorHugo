# Modelo de Programação Linear

## Variável de decisão

Para cada fornecedor `i`, `x_i` representa a quantidade do medicamento adquirida desse fornecedor.

## Função objetivo

Minimizar:

`Custo Total = Σ (preço_referencia_i × x_i)`

## Restrições

Atendimento da demanda:

`Σ x_i = D`

Limite por fornecedor:

`0 ≤ x_i ≤ L_i`

onde `D` é a demanda e `L_i` é o limite histórico estimado.

## Algoritmo

O projeto utiliza `scipy.optimize.linprog` com o método HiGHS para resolver o problema linear contínuo.

## Preparação

A base é filtrada para registros com medicamento, unidade, fornecedor, quantidade e preço válidos. Quantidades e preços são convertidos para numérico e datas para `datetime`.

## Critérios históricos

- preço de referência = mediana dos preços unitários do fornecedor;
- limite = percentil 90% das quantidades históricas do fornecedor;
- seleção padrão = cinco fornecedores com maior número de registros para o medicamento/apresentação;
- demanda padrão = 50% da soma dos limites selecionados.

## Interpretação gerencial

A solução informa quanto comprar de cada fornecedor e o custo estimado. A análise de sensibilidade recalcula o custo para demanda de -20%, -10%, 0%, +10% e +20%. A recomendação também sinaliza concentração elevada em um único fornecedor.

## Limitações

Os preços são históricos e não representam necessariamente uma cotação futura. O limite histórico é uma aproximação estatística e não uma capacidade contratual. O modelo também não incorpora frete, prazo, qualidade, tributos, validade, risco de desabastecimento ou outras regras de contratação pública.

def make_recommendation(parameters, solution, demand):
    total = solution['custo_fornecedor'].sum()
    active = solution[solution['quantidade_otima'] > 1e-6].sort_values('quantidade_otima', ascending=False)
    cheapest = parameters.loc[parameters['preco_referencia'].idxmin()]
    concentration = active['quantidade_otima'].max() / demand if demand else 0
    lines = [
        f'Custo total estimado: R$ {total:,.2f}.',
        f'Demanda atendida: {solution.quantidade_otima.sum():,.2f} unidades.',
        f'O fornecedor de menor preço de referência é {cheapest.no_fornecedor}, a R$ {cheapest.preco_referencia:,.4f} por unidade.'
    ]
    if concentration > 0.80:
        lines.append('A solução apresenta alta concentração em um fornecedor; recomenda-se avaliar risco operacional antes da contratação.')
    else:
        lines.append('A solução distribui a aquisição entre mais de um fornecedor, reduzindo a dependência de uma única fonte.')
    lines.append('Os limites são estimativas históricas (percentil 90% das quantidades por fornecedor), portanto não substituem validação contratual.')
    return lines

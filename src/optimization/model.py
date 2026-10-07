import numpy as np
from scipy.optimize import linprog


def solve_purchase(parameters, demand):
    prices = parameters['preco_referencia'].to_numpy(dtype=float)
    limits = parameters['limite_fornecimento'].to_numpy(dtype=float)
    result = linprog(prices, A_ub=np.eye(len(prices)), b_ub=limits,
                     A_eq=np.ones((1, len(prices))), b_eq=[float(demand)],
                     bounds=[(0, None)] * len(prices), method='highs')
    if not result.success:
        raise ValueError('Modelo inviável: ' + result.message)
    out = parameters.copy()
    out['quantidade_otima'] = result.x
    out['custo_fornecedor'] = out['quantidade_otima'] * out['preco_referencia']
    out['participacao'] = out['quantidade_otima'] / demand
    return result, out

import pandas as pd
from src.optimization.model import solve_purchase


def demand_sensitivity(parameters, demand, variations=(-0.20,-0.10,0,0.10,0.20)):
    rows = []
    for v in variations:
        d = demand * (1 + v)
        try:
            _, sol = solve_purchase(parameters, d)
            rows.append({'variacao_demanda': v, 'demanda': d, 'custo_total': sol.custo_fornecedor.sum(), 'viavel': True})
        except ValueError:
            rows.append({'variacao_demanda': v, 'demanda': d, 'custo_total': None, 'viavel': False})
    return pd.DataFrame(rows)

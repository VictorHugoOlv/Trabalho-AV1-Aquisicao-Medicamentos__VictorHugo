import pandas as pd
from src.optimization.model import solve_purchase

def test_solution_meets_demand_and_limits():
    p = pd.DataFrame({'preco_referencia':[10.,20.,30.], 'limite_fornecimento':[50.,50.,50.]})
    r, s = solve_purchase(p, 100)
    assert r.success
    assert abs(s.quantidade_otima.sum() - 100) < 1e-6
    assert (s.quantidade_otima <= s.limite_fornecimento + 1e-6).all()
    assert abs(s.custo_fornecedor.sum() - 1500) < 1e-6

from src.data.loader import load_bps
from src.data.preprocessing import clean_bps, available_medicines, build_parameters
from src.optimization.model import solve_purchase
from src.analysis.sensitivity import demand_sensitivity
from src.analysis.recommendation import make_recommendation


def main():
    df = clean_bps(load_bps())
    available = available_medicines(df)
    item = available.iloc[0]['ds_item']
    unit = available.iloc[0]['un_fornecimento']
    parameters, demand = build_parameters(df, item, unit, n_suppliers=5, demand_ratio=0.50)
    _, solution = solve_purchase(parameters, demand)
    sensitivity = demand_sensitivity(parameters, demand)
    parameters.to_csv('data/processed/parametros_fornecedores.csv', index=False)
    solution.to_csv('outputs/solucao_otima.csv', index=False)
    sensitivity.to_csv('outputs/sensibilidade_demanda.csv', index=False)
    with open('outputs/recomendacao.txt', 'w', encoding='utf-8') as f:
        f.write(f'Medicamento: {item}\nUnidade: {unit}\nDemanda: {demand:.2f}\nCusto total: R$ {solution.custo_fornecedor.sum():,.2f}\n\n')
        f.write('\n'.join('- ' + x for x in make_recommendation(parameters, solution, demand)))


if __name__ == '__main__':
    main()

import pandas as pd

REQUIRED = [
    'ds_item', 'un_fornecimento', 'cnpj_fornecedor', 'no_fornecedor',
    'qt_medicamento', 'vl_preco_unitario', 'dt_compra', 'sg_uf'
]


def clean_bps(df):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError('Colunas ausentes: ' + ', '.join(missing))
    out = df[REQUIRED].copy()
    out['qt_medicamento'] = pd.to_numeric(out['qt_medicamento'], errors='coerce')
    out['vl_preco_unitario'] = pd.to_numeric(out['vl_preco_unitario'], errors='coerce')
    out['dt_compra'] = pd.to_datetime(out['dt_compra'], errors='coerce', dayfirst=True)
    out = out.dropna(subset=['ds_item','un_fornecimento','cnpj_fornecedor','qt_medicamento','vl_preco_unitario'])
    out = out[(out['qt_medicamento'] > 0) & (out['vl_preco_unitario'] > 0)]
    return out


def available_medicines(df, min_suppliers=5):
    g = (df.groupby(['ds_item','un_fornecimento'])['cnpj_fornecedor']
           .nunique().reset_index(name='fornecedores'))
    return g[g['fornecedores'] >= min_suppliers].sort_values('fornecedores', ascending=False)


def build_parameters(df, item, unit, n_suppliers=5, demand_ratio=0.50):
    d = df[(df.ds_item == item) & (df.un_fornecimento == unit)].copy()
    if d.empty:
        raise ValueError('Medicamento/apresentação não encontrado.')
    stats = (d.groupby(['cnpj_fornecedor','no_fornecedor'])
        .agg(registros=('qt_medicamento','size'),
             qtd_total_historica=('qt_medicamento','sum'),
             preco_referencia=('vl_preco_unitario','median'),
             limite_fornecimento=('qt_medicamento', lambda s: s.quantile(0.90)))
        .reset_index()
        .sort_values(['registros','qtd_total_historica'], ascending=False)
        .head(n_suppliers).copy())
    demand = float(stats['limite_fornecimento'].sum() * demand_ratio)
    stats['limite_fornecimento'] = stats['limite_fornecimento'].clip(lower=1).round(2)
    return stats.reset_index(drop=True), demand

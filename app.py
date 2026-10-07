import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import streamlit as st
import matplotlib.pyplot as plt
from src.data.loader import load_bps
from src.data.preprocessing import clean_bps, available_medicines, build_parameters
from src.optimization.model import solve_purchase
from src.analysis.sensitivity import demand_sensitivity
from src.analysis.recommendation import make_recommendation
from src.ui.components import solution_table, money

st.set_page_config(page_title='SAD - Aquisição de Medicamentos', layout='wide')
st.title('💊 SAD — Aquisição de Medicamentos')
st.caption('Programação Linear aplicada à base BPS 2025')

@st.cache_data
def get_data():
    return clean_bps(load_bps())

df = get_data()
available = available_medicines(df)
items = available['ds_item'].tolist()
item = st.selectbox('Medicamento / apresentação', items, index=0)
units = available.loc[available.ds_item == item, 'un_fornecimento'].tolist()
unit = st.selectbox('Unidade de fornecimento', units)
n = st.slider('Número de fornecedores', 5, 10, 5)
ratio = st.slider('Demanda como proporção da soma dos limites históricos', 0.10, 0.90, 0.50, 0.05)

params, default_demand = build_parameters(df, item, unit, n, ratio)
demand = st.number_input('Demanda a adquirir', min_value=1.0, value=float(round(default_demand,2)), step=1.0)

if st.button('Executar otimização', type='primary'):
    try:
        result, solution = solve_purchase(params, demand)
        total = solution.custo_fornecedor.sum()
        st.success('Solução ótima encontrada.')
        c1,c2,c3 = st.columns(3)
        c1.metric('Demanda', f'{demand:,.2f}')
        c2.metric('Custo total', money(total))
        c3.metric('Fornecedores utilizados', int((solution.quantidade_otima > 1e-6).sum()))
        st.subheader('Distribuição ótima')
        st.dataframe(solution_table(solution), use_container_width=True, hide_index=True)
        fig, ax = plt.subplots()
        active = solution[solution.quantidade_otima > 1e-6]
        ax.bar(active.no_fornecedor, active.quantidade_otima)
        ax.tick_params(axis='x', rotation=35)
        ax.set_ylabel('Quantidade')
        ax.set_title('Quantidade ótima por fornecedor')
        st.pyplot(fig)
        st.subheader('Sensibilidade à demanda')
        sens = demand_sensitivity(params, demand)
        st.dataframe(sens, use_container_width=True, hide_index=True)
        fig2, ax2 = plt.subplots()
        ax2.plot(sens.demanda, sens.custo_total, marker='o')
        ax2.set_xlabel('Demanda')
        ax2.set_ylabel('Custo total')
        ax2.set_title('Custo em função da demanda')
        st.pyplot(fig2)
        st.subheader('Recomendação ao gestor')
        for line in make_recommendation(params, solution, demand): st.write('• ' + line)
        with st.expander('Formulação do modelo'):
            st.markdown('**Variável:** xᵢ = quantidade adquirida do fornecedor i.\n\n**Objetivo:** minimizar Σ(preçoᵢ × xᵢ).\n\n**Restrições:** Σxᵢ = demanda; 0 ≤ xᵢ ≤ limiteᵢ.')
    except ValueError as exc:
        st.error(str(exc))
else:
    st.info('Defina os parâmetros e clique em “Executar otimização”.')

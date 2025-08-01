import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

st.title("Simulação de Equilíbrio Eletrostático + Gravidade")

# Entradas do usuário
Q = st.number_input("Carga fixa Q (Coulombs)", value=-5e-6, format="%.2e")
q = st.number_input("Carga móvel q (Coulombs)", value=-2e-6, format="%.2e")
m = st.number_input("Massa da carga móvel m (kg)", value=0.01)
g = st.number_input("Gravidade g (m/s²)", value=9.81)

k_e = 8.99e9  # Constante eletrostática

# Função para equilíbrio
def equilibrio(y):
    Fe = k_e * abs(Q * q) / y**2
    Fg = m * g
    if Q * q > 0:
        return Fe - Fg  # Repulsiva
    else:
        return -Fe - Fg  # Atrativa

if Q * q < 0:
    st.error("❌ As forças atuam na mesma direção. Não há equilíbrio estático.")
else:
    altura_equilibrio = fsolve(equilibrio, 0.1)[0]
    st.success(f"✅ Altura de equilíbrio: {altura_equilibrio:.4f} m")

    # Gráfico de forças
    ys = np.linspace(0.01, 1.0, 500)
    Fe_vals = k_e * abs(Q * q) / ys**2
    Fg_vals = m * g * np.ones_like(ys)

    fig, ax = plt.subplots()
    ax.plot(ys, Fe_vals, label='Força Eletrostática')
    ax.plot(ys, Fg_vals, label='Força Gravitacional')
    ax.axvline(altura_equilibrio, color='red', linestyle='--', label='Equilíbrio')
    ax.set_xlabel("Altura (m)")
    ax.set_ylabel("Força (N)")
    ax.set_title("Equilíbrio entre Forças")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    # Visualização física
    fig2, ax2 = plt.subplots(figsize=(3, 6))
    ax2.set_ylim(0, max(1.1 * altura_equilibrio, 0.5))
    ax2.set_xlim(-1, 1)
    ax2.set_xticks([])

    ax2.plot(0, 0, 'ro', markersize=12, label='Carga Fixa')
    ax2.text(0.2, 0, f'Q = {Q:+.2e} C', fontsize=12, va='center')

    ax2.plot(0, altura_equilibrio, 'bo', markersize=12, label='Carga Móvel')
    ax2.text(0.2, altura_equilibrio, f'q = {q:+.2e} C', fontsize=12, va='center')

    ax2.vlines(0, 0, ax2.get_ylim()[1], colors='gray', linestyles='dotted')
    ax2.set_ylabel('Altura (m)')
    ax2.set_title('Visualização Física do Equilíbrio')
    ax2.legend(loc='center left')
    ax2.grid(True, axis='y')

    st.pyplot(fig2)

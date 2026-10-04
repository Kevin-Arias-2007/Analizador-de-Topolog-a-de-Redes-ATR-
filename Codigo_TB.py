import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Componentes Conexas", layout="wide")
st.title("Analizador de Topología de Redes (ATR)")
st.write("Generador de grafos y análisis matricial [Prototipo funcional 50%]")

if 'paso' not in st.session_state:
    st.session_state.paso = 0
if 'G' not in st.session_state:
    st.session_state.G = None
if 'pos' not in st.session_state:
    st.session_state.pos = None
if 'n' not in st.session_state:
    st.session_state.n = 6

col_izq, col_der = st.columns([1.2, 1.8])

with col_izq:
    st.subheader("1. Configuración")
    n = st.number_input("Ingrese la cantidad de nodos n:", min_value=4, max_value=12, value=st.session_state.n, step=1)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Generar Grafo Aleatorio", type="primary", use_container_width=True):
            st.session_state.n = n
            st.session_state.G = nx.gnp_random_graph(n, p=0.4)
            # AQUI GUARDAMOS LA POSICIÓN FIJA DEL GRAFO
            st.session_state.pos = nx.spring_layout(st.session_state.G)
            st.session_state.paso = 1 
    with col_btn2:
        st.button("Generar Manual", disabled=True, use_container_width=True)
        
    st.divider()
    
    if st.session_state.paso >= 1:
        st.subheader("PASO 1: Matriz de Adyacencia")
        st.write("*(Con 1s en la diagonal principal)*")
        
        A = nx.to_numpy_array(st.session_state.G, dtype=int)
        np.fill_diagonal(A, 1)
        st.code(str(A))
        
        if st.session_state.paso == 1:
            if st.button("Siguiente Paso: Calcular Matriz de Caminos", type="secondary"):
                st.session_state.paso = 2
                st.rerun() 
                
    if st.session_state.paso >= 2:
        st.subheader("PASO 2: Matriz de Caminos")
        st.write("*(Multiplicación booleana A^(n-1))*")
        
        M = np.copy(A)
        for _ in range(st.session_state.n - 1):
            M = np.dot(M, A)
        M = (M > 0).astype(int)
        st.code(str(M))
        
        st.info("**Siguientes pasos en desarrollo:**\n\n> Ordenamiento de filas por cantidad de 1s.\n\n> Ordenamiento de columnas (Bloques diagonales).")

with col_der:
    if st.session_state.paso >= 1:
        st.subheader("Visualización del Grafo")
        
        fig, ax = plt.subplots(figsize=(4, 4)) 
        nx.draw(st.session_state.G, st.session_state.pos, ax=ax, with_labels=True, node_color="#4CAF50", node_size=500, font_color="white", font_weight="bold", edge_color="gray")
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.pyplot(fig)
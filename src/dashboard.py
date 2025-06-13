import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Configurações
st.set_page_config(page_title="Dashboard Foguete PET", layout="wide")

# Caminho do CSV
dir_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(dir_path, "..", "data", "dados.csv")

# Função para carregar os dados
@st.cache_data(ttl=1)  # Atualiza a cada 1 segundo
def load_data():
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        return pd.read_csv(csv_path)
    return pd.DataFrame(columns=['lat','lon','alt','vel'])

# Título
st.title("Telemetria Foguete PET")

# Atualização automática
if st.button("Atualizar Dados"):
    # Solução para versões antigas do Streamlit
    st.experimental_memo.clear()
    st.experimental_rerun()

# Carrega os dados
df = load_data()

# Mostra dados brutos
st.subheader("Dados Brutos")
st.dataframe(df.tail(10))  # Mostra as últimas 10 leituras

# Gráficos
if not df.empty:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Altitude vs Tempo")
        st.line_chart(df.alt)
        
    with col2:
        st.subheader("Velocidade vs Tempo")
        st.line_chart(df.vel)
    
    # Trajetória 2D
    st.subheader("Trajetória Horizontal")
    if len(df) > 1:
        fig, ax = plt.subplots()
        ax.plot(df.lon, df.lat, 'b-')
        ax.plot(df.lon.iloc[0], df.lat.iloc[0], 'go', label='Início')
        ax.plot(df.lon.iloc[-1], df.lat.iloc[-1], 'ro', label='Fim')
        
        # Configurações do gráfico
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Trajetória do Foguete')
        ax.grid(True)
        ax.legend()
        
        st.pyplot(fig)
    else:
        st.warning("Dados insuficientes para mostrar trajetória")
else:
    st.warning("Aguardando dados do foguete...")

# Métricas em tempo real
if not df.empty:
    st.subheader("Métricas de Voo")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Altitude Máxima", f"{df.alt.max():.2f} m")
        
    with col2:
        st.metric("Velocidade Máxima", f"{df.vel.max():.2f} m/s")
        
    with col3:
        st.metric("Duração do Voo", f"{len(df)*0.1:.1f} s")
    
    # Análise adicional
    st.subheader("Análise do Voo")
    
    # Cálculo da aceleração
    df['acc'] = df['vel'].diff() / 0.1
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Aceleração Máxima", f"{df.acc.max():.2f} m/s²")
        
    with col2:
        st.metric("Aceleração Média", f"{df.acc.mean():.2f} m/s²")
    
    # Gráfico de aceleração
    st.subheader("Aceleração vs Tempo")
    st.line_chart(df.acc)
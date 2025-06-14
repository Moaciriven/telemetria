import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Configurações
st.set_page_config(
    page_title="Foguete PET - Telemetria em Tempo Real",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Caminho do CSV
dir_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(dir_path, "..", "data", "dados.csv")

# Função para carregar os dados
@st.cache_data(ttl=1)  # Atualiza a cada 1 segundo
def load_data():
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
        df = pd.read_csv(csv_path)
        # Adiciona timestamp para simulação de tempo real
        if 'timestamp' not in df.columns:
            start_time = datetime.now()
            df['timestamp'] = [start_time - pd.Timedelta(seconds=i*0.1) 
                              for i in range(len(df), 0, -1)]
        return df
    return pd.DataFrame(columns=['lat','lon','alt','vel','timestamp'])

# Carrega os dados
df = load_data()

# ====================
# STYLE E CONFIGURAÇÕES
# ====================
st.markdown("""
<style>
    /* Estilos gerais */
    .metric-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-radius: 12px;
        padding: 20px;
        color: white !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .metric-title {
        font-size: 1rem;
        font-weight: 300;
        color: #a0d2eb;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-unit {
        font-size: 0.9rem;
        color: #a0d2eb;
    }
    
    .section-header {
        border-left: 4px solid #2c5364;
        padding-left: 15px;
        margin: 25px 0 15px 0;
        color: #0f2027;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #203a43, #2c5364);
    }
    
    .stDataFrame {
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Cores dos gráficos */
    .altitude-color { color: #4cc9f0 }
    .velocity-color { color: #f72585 }
    .acceleration-color { color: #4361ee }
    
    /* Layout */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #203a43);
        color: white;
    }
    
    .sidebar-title {
        color: white;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==============
# BARRA LATERAL
# ==============
with st.sidebar:
    st.image("https://cdn.pixabay.com/photo/2012/04/11/18/08/rocket-29114_960_720.png", 
             width=120, caption="Foguete PET")
    
    st.title("Controle de Missão", anchor=False)
    st.subheader("Status do Sistema")
    
    # Status dos componentes
    st.markdown("""
    **Componentes:**
    - 🟢 Simulador de Voo
    - 🟢 Coletor de Dados
    - 🟢 Visualizador 3D
    - 🟢 Dashboard
    """)
    
    # Informações da missão
    st.divider()
    st.subheader("Detalhes da Missão")
    st.markdown("""
    **Nome:** PET-01  
    **Data:** 15/06/2025  
    **Local:** UFABC - São Bernardo  
    **Equipe:** Engenharia Aeroespacial  
    """)
    
    # Botão de ação
    if st.button("🛑 Abortar Missão", type="primary", use_container_width=True):
        st.warning("Comando de aborto enviado!")
    
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #a0d2eb; margin-top: 30px;">
        Sistema de Telemetria v2.1 © 2025
    </div>
    """, unsafe_allow_html=True)

# ======================
# CONTEÚDO PRINCIPAL
# ======================
st.title("🚀 Telemetria Foguete PET", anchor=False)
st.caption("Monitoramento em tempo real do voo do foguete PET-01")

# ======================
# CARDS DE MÉTRICAS
# ======================
if not df.empty:
    st.subheader("Status do Voo", divider='rainbow')
    
    # Calcula métricas
    max_alt = df.alt.max()
    max_vel = df.vel.max()
    duration = len(df) * 0.1
    current_alt = df.alt.iloc[-1]
    current_vel = df.vel.iloc[-1]
    
    # Layout dos cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ALTITUDE ATUAL</div>
            <div class="metric-value">{current_alt:.1f} <span class="metric-unit">m</span></div>
            <div style="margin-top: 10px;">
                <small>Máx: {max_alt:.1f}m</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">VELOCIDADE ATUAL</div>
            <div class="metric-value">{abs(current_vel):.1f} <span class="metric-unit">m/s</span></div>
            <div style="margin-top: 10px;">
                <small>Máx: {max_vel:.1f}m/s</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">DURAÇÃO DO VOO</div>
            <div class="metric-value">{duration:.1f} <span class="metric-unit">s</span></div>
            <div style="margin-top: 10px;">
                <small>Fase: {'DESCIDA' if current_vel < 0 else 'SUBIDA'}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">DADOS RECEBIDOS</div>
            <div class="metric-value">{len(df)} <span class="metric-unit">pontos</span></div>
            <div style="margin-top: 10px;">
                <small>{df.timestamp.iloc[-1].strftime('%H:%M:%S') if not df.empty else ''}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ======================
# GRÁFICOS PRINCIPAIS
# ======================
if not df.empty:
    st.subheader("Dados de Voo", divider='gray')
    
    # Gráficos de altitude e velocidade
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 class="altitude-color">Altitude vs Tempo</h4>', unsafe_allow_html=True)
        st.area_chart(
            df.set_index('timestamp')['alt'], 
            color='#4cc9f0',
            height=300
        )
    
    with col2:
        st.markdown('<h4 class="velocity-color">Velocidade vs Tempo</h4>', unsafe_allow_html=True)
        st.area_chart(
            df.set_index('timestamp')['vel'], 
            color='#f72585',
            height=300
        )
    
    # Trajetória 2D
    st.markdown('<h4 class="section-header">Trajetória Horizontal</h4>', unsafe_allow_html=True)
    
    if len(df) > 1:
        # Mapa de trajetória
        map_df = df[['lat', 'lon']].copy()
        map_df.columns = ['latitude', 'longitude']
        map_df['size'] = np.linspace(0.1, 10, len(df))
        
        st.map(map_df, size='size', color='#4361ee')
        
        # Gráfico de coordenadas
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df.lon, df.lat, '#4361ee', linewidth=2)
        ax.scatter(df.lon.iloc[0], df.lat.iloc[0], s=100, c='green', label='Início')
        ax.scatter(df.lon.iloc[-1], df.lat.iloc[-1], s=100, c='red', label='Fim')
        
        # Configurações do gráfico
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Trajetória do Foguete')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('#f8f9fa')
        
        st.pyplot(fig, use_container_width=True)

# ======================
# ANÁLISE DO VOO
# ======================
if not df.empty:
    st.subheader("Análise do Voo", divider='gray')
    
    # Cálculo da aceleração
    df['acc'] = df['vel'].diff() / 0.1
    
    # Layout de métricas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">ACELERAÇÃO MÁXIMA</div>
            <div class="metric-value">{df.acc.max():.1f} <span class="metric-unit">m/s²</span></div>
            <div style="margin-top: 10px;">
                <small>Lançamento</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">DESACELERAÇÃO MÁXIMA</div>
            <div class="metric-value">{df.acc.min():.1f} <span class="metric-unit">m/s²</span></div>
            <div style="margin-top: 10px;">
                <small>Reentrada</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">APOGEU</div>
            <div class="metric-value">{df.alt.max():.1f} <span class="metric-unit">m</span></div>
            <div style="margin-top: 10px;">
                <small>Altitude máxima</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráfico de aceleração
    st.markdown('<h4 class="acceleration-color">Aceleração vs Tempo</h4>', unsafe_allow_html=True)
    st.line_chart(
        df.set_index('timestamp')['acc'], 
        color='#4361ee',
        height=300
    )

# ======================
# DADOS BRUTOS
# ======================
st.subheader("Telemetria Bruta", divider='gray')
st.caption("Últimas 10 leituras recebidas")

if not df.empty:
    # Formata a tabela
    df_display = df.tail(10).copy()
    df_display['timestamp'] = df_display['timestamp'].dt.strftime('%H:%M:%S.%f')[:-3]
    df_display = df_display[['timestamp', 'lat', 'lon', 'alt', 'vel']]
    df_display.columns = ['Timestamp', 'Latitude', 'Longitude', 'Altitude (m)', 'Velocidade (m/s)']
    
    # Estiliza a tabela
    st.dataframe(
        df_display.style
        .background_gradient(subset=['Altitude (m)'], cmap='Blues')
        .background_gradient(subset=['Velocidade (m/s)'], cmap='Reds'),
        height=300
    )
    
    # Botão de download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Exportar dados completos",
        data=csv,
        file_name=f"telemetria_pet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
        use_container_width=True
    )
else:
    st.info("Aguardando dados do foguete...", icon="⏳")

# ======================
# RODAPÉ
# ======================
st.divider()
st.caption("""
**Sistema de Telemetria Foguete PET** - Desenvolvido pelo Departamento de Engenharia Aeroespacial da UFABC  
Dados atualizados em tempo real - Para uso exclusivo da equipe de controle de missão
""")
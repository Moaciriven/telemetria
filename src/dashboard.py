
import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
from datetime import datetime, timedelta
import time
import plotly.graph_objs as go

# ==============
# CONFIGURAÇÕES
# ==============
st.set_page_config(
    page_title="Foguete PET - Telemetria em Tempo Real",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Caminho do CSV
dir_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(dir_path, "..", "data", "dados.csv")

# ==============================
# ESTADO PARA LEITURA INCREMENTAL (OTIMIZADA)
# ==============================
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['lat','lon','alt','vel','timestamp'])
    st.session_state.last_size = 0
    st.session_state.last_update = time.time()

# ... (código anterior permanece igual) ...

# ==============================
# FUNÇÃO DE LEITURA INCREMENTAL (CORRIGIDA)
# ==============================
def load_data_incremental():
    try:
        if not os.path.exists(csv_path):
            st.warning(f"Arquivo não encontrado: {csv_path}")
            return
        
        current_size = os.path.getsize(csv_path)
        
        # Se o arquivo foi reiniciado (tamanho menor que antes)
        if current_size < st.session_state.last_size:
            st.session_state.df = pd.DataFrame(columns=['lat','lon','alt','vel','timestamp'])
            st.session_state.last_size = 0
            st.session_state.header_skipped = False  # Resetar flag de cabeçalho
            st.session_state.line_count = 0  # Resetar contador de linhas
        
        # Se não há dados novos
        if current_size == st.session_state.last_size:
            return
        
        # Inicializa contador de linhas se necessário
        if 'line_count' not in st.session_state:
            st.session_state.line_count = 0
        
        # Lê apenas as novas linhas
        with open(csv_path, 'r') as f:
            # Pula cabeçalho apenas na primeira leitura
            if 'header_skipped' not in st.session_state or not st.session_state.header_skipped:
                header = f.readline().strip()
                if header == "lat,lon,alt,vel":
                    st.session_state.header_skipped = True
                st.session_state.line_count += 1
            
            # Pula linhas já processadas
            for _ in range(st.session_state.line_count):
                f.readline()
            
            # Lê novas linhas
            new_lines = []
            line_count = 0
            for line in f:
                parts = line.strip().split(',')
                
                # Validação robusta dos dados
                if len(parts) == 4:
                    try:
                        # Converte para float com tratamento de locale
                        lat = float(parts[0])
                        lon = float(parts[1])
                        alt = float(parts[2])
                        vel = float(parts[3])
                        new_lines.append([lat, lon, alt, vel])
                        line_count += 1
                    except ValueError:
                        continue  # Ignora linhas com valores inválidos
            
            if new_lines:
                # Converte para DataFrame
                new_df = pd.DataFrame(new_lines, columns=['lat','lon','alt','vel'])
                
                # Atualiza contador de linhas
                st.session_state.line_count += line_count
                
                # Adiciona timestamp (usando tempo real)
                start_time = datetime.now()
                new_df['timestamp'] = [start_time - timedelta(seconds=i*0.05)
                                      for i in range(len(new_df), 0, -1)]
                
                # Atualiza o estado
                st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                st.session_state.last_size = current_size
                st.session_state.last_update = time.time()
    
    except Exception as e:
        st.error(f"Erro na leitura de dados: {str(e)}")

# ===========================
# FUNÇÃO DE PRÉ-PROCESSAMENTO (OTIMIZADA)
# ===========================
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if not df.empty:
        # Suavização mais eficiente
        df['alt_suavizada'] = df['alt'].ewm(span=5, adjust=False).mean()
        df['vel_ms'] = df['vel'] / 3.6
    return df

# ====================
# STYLE E CONFIGURAÇÕES (MELHORADO)
# ====================
st.markdown("""
<style>
    /* ===== GERAL ===== */
    .main-container {
        max-width: 95%;
        margin: 0 auto;
    }
    
    /* ===== CARDS DE MÉTRICAS ===== */
    .metric-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        border-radius: 12px;
        padding: 20px;
        color: white !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s;
        text-align: center;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: center;
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
    
    .metric-detail {
        font-size: 0.85rem;
        margin-top: 8px;
        color: #c0e0f0;
    }
    
    /* ===== SEÇÕES E TÍTULOS ===== */
    .section-header {
        border-left: 4px solid #2c5364;
        padding: 8px 15px;
        margin: 30px 0 20px 0;
        color: #0f2027;
        font-size: 1.6rem;
        font-weight: 700;
        background: linear-gradient(to right, rgba(44, 83, 100, 0.1), transparent);
        border-radius: 0 8px 8px 0;
    }
    
    .section-divider {
        height: 1px;
        background: linear-gradient(to right, transparent, #2c5364, transparent);
        margin: 25px 0;
    }
    
    .tab-section-title {
        text-align: center;
        font-size: 1.5rem;
        margin: 25px 0 20px 0;
        color: #0f2027;
        padding-bottom: 10px;
        border-bottom: 2px solid #2c5364;
        font-weight: 600;
    }
    
    /* ===== LAYOUT ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f2027, #15232b) !important;
        color: white;
        padding: 0 15px 20px 15px;
    }
    
    .sidebar-header {
        background: linear-gradient(90deg, #15232b, #2c5364);
        padding: 25px 15px;
        margin: -20px -15px 20px -15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        border-bottom: 2px solid #4cc9f0;
    }
    
    .sidebar-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 5px 0;
        letter-spacing: 1px;
    }
    
    .sidebar-subtitle {
        color: #a0d2eb;
        font-size: 1rem;
        margin-bottom: 15px;
    }
    
    .sidebar-logo {
        width: 100px;
        height: 100px;
        margin: 0 auto 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        border: 3px solid #4cc9f0;
        font-size: 50px;
    }
    
    .sidebar-section {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        box-shadow: 0 3px 8px rgba(0,0,0,0.15);
        border-left: 3px solid #4cc9f0;
    }
    
    .sidebar-section-title {
        color: #4cc9f0;
        font-size: 1.2rem;
        margin-top: 0;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
    }
    
    .sidebar-section-title i {
        margin-right: 10px;
        font-size: 1.3rem;
    }
    
    /* ===== ABAS ===== */
    .stTabs {
        margin-top: 30px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        padding: 0 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 25px;
        background: #0f2027;
        border-radius: 8px 8px 0 0;
        gap: 8px;
        font-weight: 600;
        color: #a0d2eb;
        transition: all 0.3s;
        margin: 0 2px;
        border: 1px solid #2c5364;
    }
    
    .stTabs [aria-selected="true"] {
        background: #2c5364 !important;
        color: white !important;
        border-bottom: 3px solid #4cc9f0;
    }
    
    .stTabs [aria-selected="true"] [data-testid="stMarkdownContainer"] {
        color: white !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: #1a2f38;
    }
    
    /* ===== CENTRALIZAÇÃO ===== */
    .centered-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
    }
    
    /* ===== ATUALIZAÇÃO ===== */
    .update-counter {
        position: fixed;
        bottom: 10px;
        right: 10px;
        background: rgba(15, 32, 39, 0.95);
        color: white;
        padding: 8px 15px;
        border-radius: 20px;
        font-size: 0.9rem;
        z-index: 100;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        border: 1px solid #2c5364;
        display: flex;
        align-items: center;
    }
    
    .update-icon {
        margin-right: 8px;
        font-size: 1.2rem;
        animation: pulse 1.5s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.6; }
        50% { opacity: 1; }
        100% { opacity: 0.6; }
    }
    
    /* ===== GRÁFICOS ===== */
    .chart-container {
        border-radius: 12px;
        padding: 15px;
        background: white;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    
    .chart-title {
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 15px;
        color: #0f2027;
        font-weight: 600;
    }
    
    /* ===== RODAPÉ ===== */
    .footer {
        text-align: center;
        padding: 20px 0;
        color: #5a7a8c;
        font-size: 0.9rem;
        margin-top: 40px;
        border-top: 1px solid #e0e0e0;
    }
    
    /* ===== COMPONENTES ===== */
    .status-item {
        display: flex;
        align-items: center;
        margin: 8px 0;
        padding: 8px;
        border-radius: 6px;
        background: rgba(255,255,255,0.03);
    }
    
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
    }
    
    .status-online {
        background: #00c853;
        box-shadow: 0 0 8px rgba(0,200,83,0.5);
    }
    
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #e53935, #c62828) !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
        padding: 12px !important;
        border-radius: 8px !important;
        transition: all 0.3s !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(198,40,40,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)
## ==============
# BARRA LATERAL (MODERNA E PROFISSIONAL) - CORRIGIDA
# ==============
with st.sidebar:
    # Cabeçalho da sidebar
    st.markdown("""
    <div class="sidebar-header">
        <div class="sidebar-logo">🚀</div>
        <div class="sidebar-title">FOGUETE PET</div>
        <div class="sidebar-subtitle">Sistema de Controle de Missão</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Status do sistema (CORRIGIDO)
    st.markdown("""
    <div class="sidebar-section-title">🔌 Status do Sistema</div>
    <div class="sidebar-section">
        <div class="status-item">
            <div class="status-indicator status-online"></div>
            <div>Simulador de Voo</div>
        </div>
        
        <div class="status-item">
            <div class="status-indicator status-online"></div>
            <div>Coletor de Dados</div>
        </div>
        
        <div class="status-item">
            <div class="status-indicator status-online"></div>
            <div>Trajetória com Mapa</div>
        </div>
        
        <div class="status-item">
            <div class="status-indicator status-online"></div>
            <div>Visualizador 3D</div>
        </div>
        
        <div class="status-item">
            <div class="status-indicator status-online"></div>
            <div>Dashboard</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detalhes da missão (CORRIGIDO)
    st.markdown("""
    <div class="sidebar-section-title">📋 Detalhes da Missão</div>
    <div class="sidebar-section">
        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 10px; margin-bottom: 12px;">
            <span style="color: #a0d2eb;">Nome:</span>
            <span style="font-weight: 500;">PET-01</span>
            
            <span style="color: #a0d2eb;">Data:</span>
            <span style="font-weight: 500;">01/07/2025</span>
            
            <span style="color: #a0d2eb;">Local:</span>
            <span style="font-weight: 500;">UTFPR - CM</span>
            
            <span style="color: #a0d2eb;">Equipe:</span>
            <span style="font-weight: 500;">Turma B - Física 3</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Controle de atualização
    st.markdown("""
    <div class="sidebar-section-title">⚙️ Configurações</div>
    <div class="sidebar-section">
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <div>Atualização Automática</div>
                <div style="font-weight: 500; color: #4cc9f0;">ON</div>
            </div>
            <div style="text-align: center; font-size: 0.9rem; margin-top: 5px;">Intervalo: 100ms</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Botão de abortar
    if st.button("🛑 ABORTAR MISSÃO", key="abort_button", use_container_width=True):
        st.warning("Comando de aborto enviado!")
    
    # Rodapé da sidebar
    st.markdown("""
    <div style="text-align: center; color: #5a7a8c; margin-top: 30px; font-size: 0.8rem;">
        <div style="margin-bottom: 5px;">Sistema de Telemetria v3.0</div>
        <div>© 2025 Foguete PET - UTFPR</div>
    </div>
    """, unsafe_allow_html=True)
# ======================
# ATUALIZAÇÃO DE DADOS (1000MS)
# ======================
load_data_incremental()
df = st.session_state.df
processed_df = process_data(df) if not df.empty else df

# Contador de atualização
st.markdown(f"""
<div class="update-counter">
    <span class="update-icon">⏱️</span>
    Última atualização: {datetime.now().strftime('%H:%M:%S.%f')[:-3]} | Dados: {len(df)} pontos
</div>
""", unsafe_allow_html=True)

# ======================
# CONTEÚDO PRINCIPAL
# ======================
st.title("🚀 Telemetria Foguete PET", anchor=False)
st.caption("Monitoramento em tempo real do voo do foguete PET-01")

# ======================
# SEÇÃO DE STATUS (SEMPRE VISÍVEL)
# ======================
if not df.empty:
    st.markdown('<div class="section-header">Status do Voo</div>', unsafe_allow_html=True)
    
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
            <div class="metric-detail">Máx: {max_alt:.1f} m</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">VELOCIDADE ATUAL</div>
            <div class="metric-value">{abs(current_vel):.1f} <span class="metric-unit">m/s</span></div>
            <div class="metric-detail">Máx: {max_vel:.1f} m/s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">DURAÇÃO DO VOO</div>
            <div class="metric-value">{duration:.1f} <span class="metric-unit">s</span></div>
            <div class="metric-detail">Fase: {'DESCIDA' if current_vel < 0 else 'SUBIDA'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        last_time = df.timestamp.iloc[-1].strftime('%H:%M:%S') if not df.empty else '--:--:--'
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">DADOS RECEBIDOS</div>
            <div class="metric-value">{len(df)} <span class="metric-unit">pontos</span></div>
            <div class="metric-detail">Último: {last_time}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("Aguardando dados do foguete...", icon="⏳")

# Adiciona espaço antes das abas
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# ======================
# SEÇÕES SEPARADAS EM ABAS
# ======================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 GRÁFICOS PRINCIPAIS", 
    "🌌 TRAJETÓRIA 3D", 
    "🗺️ TRAJETÓRIA 2D", 
    "📋 DADOS BRUTOS"
])

with tab1:
    # ======================
    # GRÁFICOS PRINCIPAIS
    # ======================
    if not df.empty:
        st.markdown('<div class="tab-section-title">Dados de Voo</div>', unsafe_allow_html=True)
        
        # Gráficos de altitude e velocidade
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-title centered-content">Altitude vs Tempo</div>', unsafe_allow_html=True)
            st.area_chart(
                df.set_index('timestamp')['alt'], 
                color='#4cc9f0',
                height=300
            )
        
        with col2:
            st.markdown('<div class="chart-title centered-content">Velocidade vs Tempo</div>', unsafe_allow_html=True)
            st.area_chart(
                df.set_index('timestamp')['vel'], 
                color='#f72585',
                height=300
            )
        
        # Gráfico adicional de aceleração
        st.markdown('<div class="tab-section-title">Aceleração vs Tempo</div>', unsafe_allow_html=True)
        if len(df) > 1:
            df['acceleration'] = df['vel'].diff() / 0.05  # Derivada para aceleração
            st.markdown('<div class="chart-title centered-content">Aceleração (m/s²)</div>', unsafe_allow_html=True)
            st.line_chart(
                df.set_index('timestamp')['acceleration'], 
                color='#4361ee',
                height=300
            )
        else:
            st.info("Aguardando dados suficientes para calcular aceleração", icon="ℹ️")
    else:
        st.info("Aguardando dados para exibir gráficos", icon="📊")

with tab2:
    # ======================
    # GRÁFICO 3D DE TRAJETÓRIA
    # ======================
    st.markdown('<div class="tab-section-title">Trajetória 3D</div>', unsafe_allow_html=True)
    
    if len(df) > 1:
        fig_3d = go.Figure()

        # Linha da trajetória
        fig_3d.add_trace(go.Scatter3d(
            x=df['lon'], y=df['lat'], z=df['alt'],
            mode='lines+markers',
            marker=dict(
                size=4,
                color=df['alt'],     # Colorido pela altitude
                colorscale='Viridis',
                opacity=0.8
            ),
            line=dict(
                color='#4361ee',
                width=4
            ),
            name='Trajetória'
        ))

        # Ponto de início
        fig_3d.add_trace(go.Scatter3d(
            x=[df['lon'].iloc[0]],
            y=[df['lat'].iloc[0]],
            z=[df['alt'].iloc[0]],
            mode='markers+text',
            marker=dict(size=8, color='green'),
            text=['Início'],
            textposition='bottom center',
            name='Início'
        ))

        # Ponto de fim
        fig_3d.add_trace(go.Scatter3d(
            x=[df['lon'].iloc[-1]],
            y=[df['lat'].iloc[-1]],
            z=[df['alt'].iloc[-1]],
            mode='markers+text',
            marker=dict(size=8, color='red'),
            text=['Posição Atual'],
            textposition='top center',
            name='Posição Atual'
        ))

        fig_3d.update_layout(
            scene=dict(
                xaxis_title='Longitude',
                yaxis_title='Latitude',
                zaxis_title='Altitude (m)',
                bgcolor='rgba(255,255,255,0.95)',
                xaxis=dict(showgrid=True),
                yaxis=dict(showgrid=True),
                zaxis=dict(showgrid=True),
            ),
            margin=dict(l=10, r=10, b=10, t=30),
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=dict(
                text='Trajetória 3D do Foguete',
                x=0.5,
                font=dict(color='#0f2027', size=20)
            )
        )

        st.plotly_chart(fig_3d, use_container_width=True)
    else:
        st.info("Aguardando dados suficientes para renderizar trajetória 3D", icon="🌌")

with tab3:
    # ======================
    # MAPA 2D COM GRADIENTE DE ALTITUDE
    # ======================
    st.markdown('<div class="tab-section-title">Trajetória com Gradiente de Altitude</div>', unsafe_allow_html=True)

    if len(df) > 1:
        # Criar o gráfico de mapa com Plotly
        fig_map = go.Figure()

        # Adicionar a linha de trajetória com gradiente de cor
        fig_map.add_trace(go.Scattermapbox(
            lon=df['lon'],
            lat=df['lat'],
            mode='lines+markers',
            marker=dict(
                size=8,
                color=df['alt'],  # Define a cor pelo valor da altitude
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title='Altitude (m)',
                    title_side='right',
                    thickness=15
                ),
                opacity=0.8
            ),
            line=dict(
                width=4,
                color='#4361ee'
            ),
            name='Trajetória',
            hoverinfo='text',
            hovertext='Altitude: ' + df['alt'].astype(str) + 'm<br>' +
                      'Velocidade: ' + df['vel'].astype(str) + 'm/s'
        ))

        # Ponto de início
        fig_map.add_trace(go.Scattermapbox(
            lon=[df['lon'].iloc[0]],
            lat=[df['lat'].iloc[0]],
            mode='markers+text',
            marker=dict(size=14, color='green'),
            text=['Início'],
            textposition='bottom right',
            name='Início'
        ))

        # Ponto de posição atual
        fig_map.add_trace(go.Scattermapbox(
            lon=[df['lon'].iloc[-1]],
            lat=[df['lat'].iloc[-1]],
            mode='markers+text',
            marker=dict(size=14, color='red'),
            text=['Posição Atual'],
            textposition='top left',
            name='Posição Atual'
        ))

        # Configurar o layout do mapa
        fig_map.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(
                center=dict(lat=df['lat'].mean(), lon=df['lon'].mean()),
                zoom=14
            ),
            margin=dict(l=0, r=0, t=10, b=0),
            height=600,
            title=dict(
                text='',
                x=0.5,
                font=dict(size=20, color='#0f2027')
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='closest',
            hoverlabel=dict(
                bgcolor='white',
                font_size=14,
                font_family='Arial'
            )
        )

        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.info("Aguardando dados suficientes para renderizar trajetória", icon="🗺️")

with tab4:
    # ======================
    # DADOS BRUTOS
    # ======================
    st.markdown('<div class="tab-section-title">Telemetria Bruta</div>', unsafe_allow_html=True)
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
            height=300,
            use_container_width=True
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
        st.info("Aguardando dados do foguete...", icon="📋")

# ======================
# RODAPÉ
# ======================
st.markdown("""
<div class="footer">
    <strong>Sistema de Telemetria Foguete PET</strong> - Desenvolvido por Gabriel Neves de Almeida Duarte - UTFPR<br>
    Dados atualizados em tempo real - Para uso de cunho científico da equipe de controle de dados da missão
</div>
""", unsafe_allow_html=True)

# ======================
# ATUALIZAÇÃO AUTOMÁTICA (100MS)
# ======================
time.sleep(1)
st.rerun()
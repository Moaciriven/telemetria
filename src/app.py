# app.py (arquivo principal)
import streamlit as st
import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objs as go
import numpy as np
from datetime import datetime, timedelta

# Importações de módulos locais
from styles import load_css
from components.sidebar import render_sidebar
from components.charts import plot_altitude, plot_velocity, plot_acceleration, plot_3d_trajectory, plot_2d_trajectory
from components.data_loader import load_data_incremental, process_data

# ==============
# CONFIGURAÇÕES
# ==============
st.set_page_config(
    page_title="Foguete PET - Telemetria em Tempo Real",
    layout="wide",
    page_icon="🚀",
    initial_sidebar_state="expanded"
)

# Carregar estilos CSS
load_css()

# ==============================
# ESTADO PARA LEITURA INCREMENTAL
# ==============================
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['lat','lon','alt','vel','timestamp'])
    st.session_state.last_size = 0
    st.session_state.last_update = time.time()

# ======================
# ATUALIZAÇÃO DE DADOS
# ======================
load_data_incremental()
df = st.session_state.df
processed_df = process_data(df) if not df.empty else df

# ======================
# BARRA LATERAL
# ======================
render_sidebar()

# Contador de atualização
st.markdown(f"""
<div class="update-counter">
    <span>⏱️</span> Última atualização: {datetime.now().strftime('%H:%M:%S.%f')[:-3]} | Dados: {len(df)} pontos
</div>
""", unsafe_allow_html=True)

# ======================
# CONTEÚDO PRINCIPAL
# ======================
st.title("🚀 Telemetria Foguete PET")
st.caption("Monitoramento em tempo real do voo do foguete PET-01")

# ======================
# SEÇÃO DE STATUS
# ======================
if not df.empty:
    st.markdown('<div class="section-header">Status do Voo</div>', unsafe_allow_html=True)
    
    max_alt = df.alt.max()
    max_vel = df.vel.max()
    duration = len(df) * 0.1
    current_alt = df.alt.iloc[-1]
    current_vel = df.vel.iloc[-1]
    
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

st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

# ======================
# SEÇÕES EM ABAS
# ======================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 GRÁFICOS PRINCIPAIS", 
    "🌌 TRAJETÓRIA 3D", 
    "🗺️ TRAJETÓRIA 2D", 
    "📋 DADOS BRUTOS"
])

with tab1:
    if not df.empty:
        st.markdown('<div class="tab-section-title">Dados de Voo</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-title">Altitude vs Tempo</div>', unsafe_allow_html=True)
            plot_altitude(df)
        
        with col2:
            st.markdown('<div class="chart-title">Velocidade vs Tempo</div>', unsafe_allow_html=True)
            plot_velocity(df)
        
        st.markdown('<div class="tab-section-title">Aceleração vs Tempo</div>', unsafe_allow_html=True)
        if len(df) > 1:
            st.markdown('<div class="chart-title">Aceleração (m/s²)</div>', unsafe_allow_html=True)
            plot_acceleration(df)
        else:
            st.info("Aguardando dados suficientes para calcular aceleração", icon="ℹ️")
    else:
        st.info("Aguardando dados para exibir gráficos", icon="📊")

with tab2:
    st.markdown('<div class="tab-section-title">TRAJETÓRIA DO FOGUETE PET</div>', unsafe_allow_html=True)
    if len(df) > 1:
        plot_3d_trajectory(df)
    else:
        st.info("AGUARDANDO DADOS PARA VISUALIZAÇÃO DA TRAJETÓRIA", icon="📡")
        
with tab3:
    st.markdown('<div class="tab-section-title">Trajetória com Gradiente de Altitude</div>', unsafe_allow_html=True)
    if len(df) > 1:
        plot_2d_trajectory(df)
    else:
        st.info("Aguardando dados suficientes para renderizar trajetória", icon="🗺️")

with tab4:
    st.markdown('<div class="tab-section-title">Telemetria Bruta</div>', unsafe_allow_html=True)
    st.caption("Últimas 10 leituras recebidas")

    if not df.empty:
        df_display = df.tail(10).copy()
        df_display['timestamp'] = df_display['timestamp'].dt.strftime('%H:%M:%S.%f')[:-3]
        df_display = df_display[['timestamp', 'lat', 'lon', 'alt', 'vel']]
        df_display.columns = ['Timestamp', 'Latitude', 'Longitude', 'Altitude (m)', 'Velocidade (m/s)']
        
        st.dataframe(
            df_display.style
            .background_gradient(subset=['Altitude (m)'], cmap='Blues')
            .background_gradient(subset=['Velocidade (m/s)'], cmap='Reds'),
            height=300,
            use_container_width=True
        )
        
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
# ATUALIZAÇÃO AUTOMÁTICA
# ======================
time.sleep(5)
st.rerun()
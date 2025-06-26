# components/sidebar.py
import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="
                background: linear-gradient(90deg, #15232b, #2c5364);
                padding: 25px 15px;
                margin: -20px -15px 20px -15px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                border-bottom: 2px solid #4cc9f0;
            ">
                <div style="
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
                ">🚀</div>
                <div style="color: white; font-size: 1.8rem; font-weight: 700; margin: 5px 0; letter-spacing: 1px;">
                    FOGUETE PET
                </div>
                <div style="color: #a0d2eb; font-size: 1rem; margin-bottom: 15px;">
                    Sistema de Controle de Missão
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.subheader("🔌 Status do Sistema")
        cols = st.columns([0.1, 0.9])
        with cols[0]: st.markdown('<div style="background: #00c853; width: 12px; height: 12px; border-radius: 50%; margin-top: 8px;"></div>', unsafe_allow_html=True)
        with cols[1]: st.write("Simulador de Voo")
        
        cols = st.columns([0.1, 0.9])
        with cols[0]: st.markdown('<div style="background: #00c853; width: 12px; height: 12px; border-radius: 50%; margin-top: 8px;"></div>', unsafe_allow_html=True)
        with cols[1]: st.write("Coletor de Dados")
        
        cols = st.columns([0.1, 0.9])
        with cols[0]: st.markdown('<div style="background: #00c853; width: 12px; height: 12px; border-radius: 50%; margin-top: 8px;"></div>', unsafe_allow_html=True)
        with cols[1]: st.write("Trajetória com Mapa")
        
        cols = st.columns([0.1, 0.9])
        with cols[0]: st.markdown('<div style="background: #00c853; width: 12px; height: 12px; border-radius: 50%; margin-top: 8px;"></div>', unsafe_allow_html=True)
        with cols[1]: st.write("Visualizador 3D")
        
        cols = st.columns([0.1, 0.9])
        with cols[0]: st.markdown('<div style="background: #00c853; width: 12px; height: 12px; border-radius: 50%; margin-top: 8px;"></div>', unsafe_allow_html=True)
        with cols[1]: st.write("Dashboard")
        
        st.subheader("📋 Detalhes da Missão")
        col1, col2 = st.columns(2)
        col1.markdown('<div style="color: #a0d2eb;">Nome:</div>', unsafe_allow_html=True)
        col2.markdown('<div style="font-weight: 500;">PET-01</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.markdown('<div style="color: #a0d2eb;">Data:</div>', unsafe_allow_html=True)
        col2.markdown('<div style="font-weight: 500;">01/07/2025</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.markdown('<div style="color: #a0d2eb;">Local:</div>', unsafe_allow_html=True)
        col2.markdown('<div style="font-weight: 500;">UTFPR - CM</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        col1.markdown('<div style="color: #a0d2eb;">Equipe:</div>', unsafe_allow_html=True)
        col2.markdown('<div style="font-weight: 500;">Turma B - Física 3</div>', unsafe_allow_html=True)
        
        st.subheader("⚙️ Configurações")
        col1, col2 = st.columns([0.7, 0.3])
        col1.write("Atualização Automática")
        col2.markdown('<div style="font-weight: 500; color: #4cc9f0;">ON</div>', unsafe_allow_html=True)
        st.caption("Intervalo: 100ms")
        
        if st.button("🛑 ABORTAR MISSÃO", key="abort_button", use_container_width=True):
            st.warning("Comando de aborto enviado!")
        
        st.markdown(
            """
            <div style="text-align: center; color: #5a7a8c; margin-top: 30px; font-size: 0.8rem;">
                <div style="margin-bottom: 5px;">Sistema de Telemetria v3.0</div>
                <div>© 2025 Foguete PET - UTFPR</div>
            </div>
            """,
            unsafe_allow_html=True
        )
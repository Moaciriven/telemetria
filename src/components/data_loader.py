# components/data_loader.py
import os
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import time

# Caminho do CSV
dir_path = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(dir_path, "..", "..", "data", "dados.csv")

def load_data_incremental():
    try:
        if not os.path.exists(csv_path):
            st.warning(f"Arquivo não encontrado: {csv_path}")
            return
        
        current_size = os.path.getsize(csv_path)
        
        if current_size < st.session_state.last_size:
            st.session_state.df = pd.DataFrame(columns=['lat','lon','alt','vel','timestamp'])
            st.session_state.last_size = 0
            st.session_state.header_skipped = False
            st.session_state.line_count = 0
        
        if current_size == st.session_state.last_size:
            return
        
        if 'line_count' not in st.session_state:
            st.session_state.line_count = 0
        
        with open(csv_path, 'r') as f:
            if 'header_skipped' not in st.session_state or not st.session_state.header_skipped:
                header = f.readline().strip()
                if header == "lat,lon,alt,vel":
                    st.session_state.header_skipped = True
                st.session_state.line_count += 1
            
            for _ in range(st.session_state.line_count):
                f.readline()
            
            new_lines = []
            line_count = 0
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 4:
                    try:
                        lat = float(parts[0])
                        lon = float(parts[1])
                        alt = float(parts[2])
                        vel = float(parts[3])
                        new_lines.append([lat, lon, alt, vel])
                        line_count += 1
                    except ValueError:
                        continue
            
            if new_lines:
                new_df = pd.DataFrame(new_lines, columns=['lat','lon','alt','vel'])
                st.session_state.line_count += line_count
                
                start_time = datetime.now()
                new_df['timestamp'] = pd.date_range(
                    start=start_time - timedelta(seconds=len(new_df)*0.05), 
                    end=start_time, 
                    periods=len(new_df)
                )
                
                st.session_state.df = pd.concat([st.session_state.df, new_df], ignore_index=True)
                st.session_state.last_size = current_size
                st.session_state.last_update = time.time()
    
    except Exception as e:
        st.error(f"Erro na leitura de dados: {str(e)}")

def process_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if not df.empty:
        df['alt_suavizada'] = df['alt'].ewm(span=5, adjust=False).mean()
        df['vel_ms'] = df['vel'] / 3.6
    return df
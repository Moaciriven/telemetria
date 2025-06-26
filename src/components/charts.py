# components/charts.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objs as go
import numpy as np

def plot_altitude(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['timestamp'], df['alt'], color='#4cc9f0')
    ax.fill_between(df['timestamp'], df['alt'], alpha=0.3, color='#4cc9f0')
    ax.set_ylabel('Altitude (m)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def plot_velocity(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['timestamp'], df['vel'], color='#f72585')
    ax.fill_between(df['timestamp'], df['vel'], alpha=0.3, color='#f72585')
    ax.set_ylabel('Velocidade (m/s)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def plot_acceleration(df):
    df['acceleration'] = df['vel'].diff() / 0.05
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['timestamp'], df['acceleration'], color='#4361ee')
    ax.set_ylabel('Aceleração (m/s²)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

def plot_3d_trajectory(df):
    MAX_ALT = df['alt'].max() + 5
    MIN_ALT = min(df['alt'].min(), 0) - 1
    
    fig_3d = go.Figure()

    # Trajetória principal
    fig_3d.add_trace(go.Scatter3d(
        x=df['lon'],
        y=df['lat'],
        z=df['alt'],
        mode='lines+markers',
        marker=dict(
            size=4,
            color=df['alt'],
            colorscale='Jet',
            cmin=0,
            cmax=MAX_ALT,
            showscale=True,
            colorbar=dict(title='Altitude (m)', thickness=15, x=0.82, y=0.3)
        ),
        line=dict(width=8, color=df['alt'], colorscale='Jet'),
        name='Trajetória',
        hoverinfo='text',
        hovertext=[f"Alt: {alt:.1f}m<br>Lat: {lat:.6f}°<br>Lon: {lon:.6f}°" 
                  for alt, lat, lon in zip(df['alt'], df['lat'], df['lon'])]
    ))

    # Pontos importantes
    # (Ponto de lançamento, pico e aterrissagem)
    
    # Layout
    fig_3d.update_layout(
        scene=dict(
            xaxis=dict(title='Longitude (°)', gridcolor='rgba(100, 100, 100, 0.2)'),
            yaxis=dict(title='Latitude (°)', gridcolor='rgba(100, 100, 100, 0.2)'),
            zaxis=dict(title='Altitude (m)', gridcolor='rgba(100, 100, 100, 0.2)', range=[MIN_ALT, MAX_ALT * 1.1]),
            bgcolor='#0a1020',
            aspectmode='manual',
            aspectratio=dict(x=2, y=1, z=0.8),
            camera=dict(eye=dict(x=1.5, y=-1.5, z=0.8), up=dict(x=0, y=0, z=1))
        ),
        height=650,
        margin=dict(l=20, r=20, b=20, t=20),
        font=dict(family="Arial", size=12, color="white"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        paper_bgcolor='#0a1020',
        hoverlabel=dict(bgcolor='rgba(10, 15, 30, 0.9)', font_size=12)
    )

    st.plotly_chart(fig_3d, use_container_width=True)

def plot_2d_trajectory(df):
    fig_map = go.Figure()
    
    fig_map.add_trace(go.Scattermapbox(
        lon=df['lon'], lat=df['lat'],
        mode='lines+markers',
        marker=dict(
            size=10,
            color=df['alt'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Altitude (m)', title_side='right', thickness=15),
            opacity=0.9
        ),
        line=dict(width=5, color='#4361ee'),
        name='Trajetória',
        hoverinfo='text',
        hovertext='Altitude: ' + df['alt'].astype(str) + 'm<br>Velocidade: ' + df['vel'].astype(str) + 'm/s'
    ))

    fig_map.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(center=dict(lat=df['lat'].mean(), lon=df['lon'].mean()), zoom=14),
        margin=dict(l=0, r=0, t=10, b=0),
        height=600,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor='white', font_size=14, font_family='Arial')
    )

    st.plotly_chart(fig_map, use_container_width=True)
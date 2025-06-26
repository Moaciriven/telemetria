# styles.py
import streamlit as st

def load_css():
    st.markdown("""
    <style>
        /* ESTILOS GERAIS */
        .metric-card {
            background: linear-gradient(135deg, #0a1a23, #152a35, #1d3c4a);
            border-radius: 12px;
            padding: 20px;
            color: white !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            text-align: center;
            height: 130px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        .metric-title {
            font-size: 1rem;
            font-weight: 600;
            color: #4cc9f0;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        }
        
        .metric-unit {
            font-size: 0.9rem;
            color: #a0d2eb;
            font-weight: 600;
        }
        
        .metric-detail {
            font-size: 0.85rem;
            margin-top: 8px;
            color: #c0e0f0;
            font-weight: 500;
        }
        
        .section-header {
            border-left: 4px solid #2c5364;
            padding: 8px 15px;
            margin: 30px 0 20px 0;
            color: #0a141a;
            font-size: 1.6rem;
            font-weight: 700;
            background: linear-gradient(to right, rgba(44, 83, 100, 0.15), transparent);
            border-radius: 0 8px 8px 0;
        }
        
        .tab-section-title {
            text-align: center;
            font-size: 1.5rem;
            margin: 25px 0 20px 0;
            color: #0a141a;
            padding-bottom: 10px;
            border-bottom: 3px solid #2c5364;
            font-weight: 700;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f2027, #15232b) !important;
            color: white;
            padding: 0 15px 20px 15px;
        }
        
        .update-counter {
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: rgba(10, 26, 35, 0.95);
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            border: 1px solid #2c5364;
            display: flex;
            align-items: center;
            font-weight: 600;
        }
        
        .chart-title {
            text-align: center;
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: #0a141a !important;
            font-weight: 700;
        }
        
        .footer {
            text-align: center;
            padding: 20px 0;
            color: #5a7a8c;
            font-size: 0.9rem;
            margin-top: 40px;
            border-top: 1px solid #e0e0e0;
        }
        
        /* ESTILOS ESPECÍFICOS PARA DASHBOARD */
        .metric-card {
            background-color: rgba(0, 0, 0, 0.7) !important;
            padding: 10px;
            border-radius: 8px;
            color: white !important;
            box-shadow: 0 0 8px rgba(0,0,0,0.8);
        }

        .section-header {
            color: white !important;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 12px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        }

        .metric-title {
            color: white !important;
            font-weight: 700;
            font-size: 14px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        }

        .metric-value {
            color: white !important;
            font-size: 22px;
            font-weight: 600;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        }

        .metric-detail {
            color: #ddd !important;
            font-size: 12px;
            font-weight: 400;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        .tab-section-title {
            color: white !important;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 12px;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        }

        .chart-title {
            color: white !important;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 8px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.6);
        }
    </style>
    """, unsafe_allow_html=True)
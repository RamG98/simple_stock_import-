import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- Load CSV ---
st.title("📈 Interactive Stock Chart Viewer")

uploaded_file = st.file_uploader("Upload your stock CSV (must include 'Date' and 'Close')", type='csv')

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=['Date'])

    # --- Date Range Filter ---
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()

    start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

    if start_date > end_date:
        st.error("Start date must be before end date.")
    else:
        filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        # --- Plotly Chart ---
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=filtered['Date'],
            y=filtered['Close'],
            mode='lines',
            name='Close Price'
        ))

        fig.update_layout(
            title="Stock Price Over Time",
            xaxis_title="Date",
            yaxis_title="Price",
            dragmode='drawopenpath',  # Enables drawing
            newshape_line_color='red',
            showlegend=True,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

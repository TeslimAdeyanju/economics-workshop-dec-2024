import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils import load_data, get_chart_layout

def show():
    st.header('Stock Market Overview')
    
    try:
        # Load S&P 500 data
        sp500_query = """
        SELECT *
        FROM sp500
        ORDER BY date
        """
        sp500 = load_data(sp500_query)
        
        if not sp500.empty and sp500['SP500'].notna().any():
            st.subheader('S&P 500 Index with Moving Averages')
            latest_sp500 = sp500['SP500'].iloc[-1]
            latest_ma200 = sp500['sp500_ma200'].iloc[-1]
            latest_date = sp500.index[-1]
            
            caption = f'<span style="background-color: #31333F; padding: 2px 6px; border-radius: 3px;"><b>Latest data: {latest_date.strftime("%B %Y")}</b></span>'
            if pd.notna(latest_sp500):
                caption += f' | S&P 500: {latest_sp500:,.0f}'
            if pd.notna(latest_ma200):
                caption += f' | MA200: {latest_ma200:,.0f}'
            st.caption(caption, unsafe_allow_html=True)
            
            fig_sp500 = go.Figure()
            fig_sp500.add_trace(go.Scatter(
                x=sp500.index, 
                y=sp500['SP500'],
                name='S&P 500',
                line=dict(color='#FFBA08', width=2),
                hovertemplate='Date: %{x}<br>S&P 500: %{y:,.0f}<extra></extra>'
            ))
            fig_sp500.add_trace(go.Scatter(
                x=sp500.index, 
                y=sp500['sp500_ma20'],
                name='20-day MA',
                line=dict(color='#00FFF0', width=1, dash='dash'),
                hovertemplate='Date: %{x}<br>20-day MA: %{y:,.0f}<extra></extra>'
            ))
            fig_sp500.add_trace(go.Scatter(
                x=sp500.index, 
                y=sp500['sp500_ma50'],
                name='50-day MA',
                line=dict(color='#FF00FF', width=1, dash='dash'),
                hovertemplate='Date: %{x}<br>50-day MA: %{y:,.0f}<extra></extra>'
            ))
            fig_sp500.add_trace(go.Scatter(
                x=sp500.index, 
                y=sp500['sp500_ma200'],
                name='200-day MA',
                line=dict(color='#00FF00', width=1, dash='dash'),
                hovertemplate='Date: %{x}<br>200-day MA: %{y:,.0f}<extra></extra>'
            ))
            fig_sp500.update_layout(get_chart_layout(''))
            st.plotly_chart(fig_sp500, use_container_width=True)
            
            # Add S&P 500 commentary
            st.markdown("""
            * **Technical Overview**: The S&P 500 tracks 500 large U.S. companies, with moving averages (20-day, 50-day, and 200-day) showing trend strength and momentum.
            * **Market Context**: Moving averages help identify market trends - when price is above longer-term averages, it suggests an uptrend; below suggests a downtrend.
            * **Historical Perspective**: Despite periodic downturns (like 2008, 2020), the index shows a long-term upward trend, reflecting overall economic growth.
            * **Retail Investor**: Consider the 200-day moving average as a key reference - when S&P 500 is above it, maintain regular investments; when below, you might gradually increase positions during dips while keeping some cash reserve.
            """)

        # VIX
        vix_query = """
        SELECT *
        FROM vixcls
        ORDER BY date
        """
        vix = load_data(vix_query)
        
        if not vix.empty and vix['VIXCLS'].notna().any():
            vix['vix_ma20'] = vix['VIXCLS'].rolling(window=20).mean()
            vix['vix_ma50'] = vix['VIXCLS'].rolling(window=50).mean()
            
            st.subheader('VIX Volatility Index')
            latest_vix = vix['VIXCLS'].iloc[-1]
            latest_vix_ma20 = vix['vix_ma20'].iloc[-1]
            latest_date = vix.index[-1]
            
            caption = f'<span style="background-color: #31333F; padding: 2px 6px; border-radius: 3px;"><b>Latest data: {latest_date.strftime("%B %Y")}</b></span>'
            if pd.notna(latest_vix):
                caption += f' | VIX: {latest_vix:.1f}'
            if pd.notna(latest_vix_ma20):
                caption += f' | MA20: {latest_vix_ma20:.1f}'
            st.caption(caption, unsafe_allow_html=True)
            
            fig_vix = go.Figure()
            fig_vix.add_trace(go.Scatter(
                x=vix.index, 
                y=vix['VIXCLS'],
                name='VIX',
                line=dict(color='#FFBA08', width=2),
                hovertemplate='Date: %{x}<br>VIX: %{y:.1f}<extra></extra>'
            ))
            fig_vix.add_trace(go.Scatter(
                x=vix.index, 
                y=vix['vix_ma20'],
                name='20-day MA',
                line=dict(color='#00FFF0', width=1, dash='dash'),
                hovertemplate='Date: %{x}<br>20-day MA: %{y:.1f}<extra></extra>'
            ))
            fig_vix.add_trace(go.Scatter(
                x=vix.index, 
                y=vix['vix_ma50'],
                name='50-day MA',
                line=dict(color='#FF00FF', width=1, dash='dash'),
                hovertemplate='Date: %{x}<br>50-day MA: %{y:.1f}<extra></extra>'
            ))
            fig_vix.update_layout(get_chart_layout(''))
            st.plotly_chart(fig_vix, use_container_width=True)

            # Add VIX commentary
            st.markdown("""
            * **Market Fear Gauge**: The VIX measures expected market volatility, with higher values indicating uncertainty and lower values suggesting stability.
            * **Historical Context**: Major spikes (like in 2008, 2020) typically coincide with significant market events or crises.
            * **Trend Analysis**: The moving averages help identify if volatility is increasing or decreasing over time.
            * **Retail Investor**: High VIX levels (above 30) often present buying opportunities, but enter gradually. Very low VIX (below 15) might signal market complacency - consider taking some profits or maintaining a balanced portfolio.
            """)

    except Exception as e:
        st.error(f"Error in Stock Market Overview: {str(e)}")

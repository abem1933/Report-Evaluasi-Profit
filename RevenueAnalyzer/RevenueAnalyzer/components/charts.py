import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def render_charts(df, metrics, calculator):
"""Render various charts for financial analysis"""
st.subheader("📊 Analisis Grafik")

```
if df.empty:
    st.warning("⚠️ Tidak ada data untuk ditampilkan dalam grafik.")
    return

# Monthly trends
monthly_data = metrics['monthly_data']

if not monthly_data.empty:
    render_monthly_trends(monthly_data)
    render_profit_analysis(monthly_data)
    render_expense_trends(monthly_data)

# Daily/detailed trends if enough data points
if len(df) > 7:
    render_daily_trends(df)

# Category analysis if categories exist
if 'Kategori' in df.columns and len(df['Kategori'].unique()) > 1:
    render_category_analysis(df)

# Customer analysis if customers exist
if 'Nama_Customer' in df.columns and len(df['Nama_Customer'].unique()) > 1:
    render_customer_analysis(df)
```

def render_monthly_trends(monthly_data):
"""Render monthly revenue and profit trends"""
st.markdown("#### 📈 Tren Bulanan - Revenue & Profit")

```
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Revenue vs COGS', 'Profit Trends'),
    vertical_spacing=0.1
)

fig.add_trace(go.Scatter(
    x=monthly_data['Month'], y=monthly_data['Revenue'],
    name='Revenue', line=dict(color='#2E86C1', width=3), mode='lines+markers'
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=monthly_data['Month'], y=monthly_data['COGS'],
    name='COGS', line=dict(color='#E74C3C', width=3), mode='lines+markers'
), row=1, col=1)

fig.add_trace(go.Scatter(
    x=monthly_data['Month'], y=monthly_data['Gross_Profit'],
    name='Gross Profit', line=dict(color='#28B463', width=3), mode='lines+markers'
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=monthly_data['Month'], y=monthly_data['Net_Profit'],
    name='Net Profit', line=dict(color='#8E44AD', width=3), mode='lines+markers'
), row=2, col=1)

fig.update_layout(height=600, title_text="Tren Keuangan Bulanan", showlegend=True)
fig.update_xaxes(title_text="Bulan", row=2, col=1)
fig.update_yaxes(title_text="Jumlah (Rp)", row=1, col=1)
fig.update_yaxes(title_text="Profit (Rp)", row=2, col=1)

st.plotly_chart(fig, use_container_width=True)
```

def render_profit_analysis(monthly_data):
"""Render profit margin analysis"""
st.markdown("#### 💹 Analisis Margin Profit")

```
col1, col2 = st.columns(2)

with col1:
    fig_margin = go.Figure()
    fig_margin.add_trace(go.Scatter(
        x=monthly_data['Month'], y=monthly_data['Gross_Margin'],
        name='Gross Margin (%)', line=dict(color='#F39C12', width=3), mode='lines+markers'
    ))
    fig_margin.add_trace(go.Scatter(
        x=monthly_data['Month'], y=monthly_data['Net_Margin'],
        name='Net Margin (%)', line=dict(color='#9B59B6', width=3), mode='lines+markers'
    ))
    fig_margin.update_layout(title="Tren Margin Profit", xaxis_title="Bulan", yaxis_title="Margin (%)", height=400)
    st.plotly_chart(fig_margin, use_container_width=True)

with col2:
    latest_month = monthly_data.iloc[-1] if not monthly_data.empty else None
    if latest_month is not None:
        profit_data = {
            'Kategori': ['Gross Profit', 'Komisi Penjualan', 'Program Penjualan'],
            'Nilai': [
                latest_month['Gross_Profit'],
                latest_month['Sales_Commission'],
                latest_month['Sales_Program']
            ]
        }
        fig_waterfall = go.Figure(go.Waterfall(
            name="Profit Breakdown", orientation="v",
            measure=["relative", "relative", "relative", "total"],
            x=["Gross Profit", "Komisi Penjualan", "Program Penjualan", "Net Profit"],
            textposition="outside",
            text=[f"Rp {val:,.0f}" for val in profit_data['Nilai']] + [f"Rp {latest_month['Net_Profit']:,.0f}"],
            y=[latest_month['Gross_Profit'], -latest_month['Sales_Commission'], 
               -latest_month['Sales_Program'], latest_month['Net_Profit']],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        fig_waterfall.update_layout(title=f"Waterfall Profit - {latest_month['Month']}", showlegend=False, height=400)
        st.plotly_chart(fig_waterfall, use_container_width=True)
```

def render_expense_trends(monthly_data):
"""Render expense trends analysis"""
st.markdown("#### 💸 Tren Pengeluaran")

```
# Stacked area chart
fig_expenses = go.Figure()
fig_expenses.add_trace(go.Scatter(
    x=monthly_data['Month'], y=monthly_data['COGS'],
    fill='tonexty', mode='lines', name='COGS',
    line=dict(width=0.5, color='rgb(131, 90, 241)'), stackgroup='one'
))
fig_expenses.add_trace(go.Scatter(
    x=monthly_data['Month'], y=monthly_data['Sales_Commission'],
    fill='tonexty', mode='lines', name='Komisi Penjualan',
    line=dict(width=0.5, color='rgb(111, 231, 219)'), stackgroup='one'
))
fig_expenses.add_trace(go.Scatter(
    x=monthly_data['Month'], y=monthly_data['Sales_Program'],
    fill='tonexty', mode='lines', name='Program Penjualan',
    line=dict(width=0.5, color='rgb(255, 166, 0)'), stackgroup='one'
))
fig_expenses.update_layout(title="Komposisi Pengeluaran Bulanan", xaxis_title="Bulan", yaxis_title="Jumlah (Rp)", height=400)
st.plotly_chart(fig_expenses, use_container_width=True)

# Breakdown pengeluaran
st.markdown("#### 🧾 Breakdown Pengeluaran")
latest_month = monthly_data.iloc[-1] if not monthly_data.empty else None
if latest_month is not None:
    expense_data = {
        'Kategori': ['COGS', 'Komisi Penjualan', 'Program Penjualan'],
        'Jumlah': [
            latest_month['COGS'],
            latest_month['Sales_Commission'],
            latest_month['Sales_Program']
        ]
    }
    expense_df = pd.DataFrame(expense_data)
    total_expense = expense_df['Jumlah'].sum()
    expense_df['Persentase'] = (expense_df['Jumlah'] / total_expense * 100).round(2)

    col1, col2 = st.columns(2)
    with col1:
        fig_pie = px.pie(expense_df, values='Jumlah', names='Kategori',
            title="Distribusi Pengeluaran", color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_bar = px.bar(expense_df, x='Kategori', y='Jumlah',
            title="Jumlah Pengeluaran per Kategori",
            text=expense_df['Jumlah'].apply(lambda x: f"Rp {x:,.0f}"),
            color='Kategori', color_discrete_sequence=px.colors.qualitative.Set3)
        fig_bar.update_layout(xaxis_title="Kategori", yaxis_title="Jumlah (Rp)")
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("#### 📊 Persentase terhadap Total Pengeluaran")
    expense_df_display = expense_df.copy()
    expense_df_display['Jumlah'] = expense_df_display['Jumlah'].apply(lambda x: f"Rp {x:,.0f}")
    expense_df_display['Persentase'] = expense_df_display['Persentase'].apply(lambda
```

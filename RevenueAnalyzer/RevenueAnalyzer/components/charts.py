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
st.markdown("#### 📈 Tren Bulanan - Revenue & Profit")
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

def render_profit_analysis(monthly_data):
st.markdown("#### 💹 Analisis Margin Profit")
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
if not monthly_data.empty:
latest_month = monthly_data.iloc[-1]
fig_waterfall = go.Figure(go.Waterfall(
name="Profit Breakdown", orientation="v",
measure=["relative", "relative", "relative", "total"],
x=["Gross Profit", "Komisi Penjualan", "Program Penjualan", "Net Profit"],
textposition="outside",
text=[
f"Rp {latest_month['Gross_Profit']:,.0f}",
f"Rp {latest_month['Sales_Commission']:,.0f}",
f"Rp {latest_month['Sales_Program']:,.0f}",
f"Rp {latest_month['Net_Profit']:,.0f}"
],
y=[latest_month['Gross_Profit'], -latest_month['Sales_Commission'],
-latest_month['Sales_Program'], latest_month['Net_Profit']],
connector={"line": {"color": "rgb(63, 63, 63)"}}
))
fig_waterfall.update_layout(title=f"Waterfall Profit - {latest_month['Month']}", showlegend=False, height=400)
st.plotly_chart(fig_waterfall, use_container_width=True)

def render_expense_trends(monthly_data):
st.markdown("#### 💸 Tren Pengeluaran")
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

```
st.markdown("#### 🧾 Breakdown Pengeluaran")
if not monthly_data.empty:
    latest_month = monthly_data.iloc[-1]
    expense_df = pd.DataFrame({
        'Kategori': ['COGS', 'Komisi Penjualan', 'Program Penjualan'],
        'Jumlah': [latest_month['COGS'], latest_month['Sales_Commission'], latest_month['Sales_Program']]
    })
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
    expense_df_display['Persentase'] = expense_df_display['Persentase'].apply(lambda x: f"{x:.2f}%")
    st.table(expense_df_display)
```

def render_daily_trends(df):
st.markdown("#### 📅 Tren Harian")
df_daily = df.set_index('Tanggal').resample('D').agg({
'Revenue': 'sum','COGS': 'sum','Sales_Commission': 'sum','Sales_Program': 'sum'
}).reset_index()
df_daily['Net_Profit'] = df_daily['Revenue'] - df_daily['COGS'] - df_daily['Sales_Commission'] - df_daily['Sales_Program']
df_daily = df_daily[df_daily['Revenue'] > 0]
if not df_daily.empty and len(df_daily) > 1:
fig_daily = px.line(df_daily, x='Tanggal', y=['Revenue','Net_Profit'],
title="Tren Harian - Revenue vs Net Profit",
color_discrete_map={'Revenue': '#3498DB','Net_Profit': '#E74C3C'})
fig_daily.update_layout(xaxis_title="Tanggal", yaxis_title="Jumlah (Rp)", height=400)
st.plotly_chart(fig_daily, use_container_width=True)

def render_category_analysis(df):
st.markdown("#### 🏷️ Analisis per Kategori")
category_summary = df.groupby('Kategori').agg({
'Revenue':'sum','COGS':'sum','Sales_Commission':'sum','Sales_Program':'sum'
}).reset_index()
category_summary['Gross_Profit'] = category_summary['Revenue'] - category_summary['COGS']
category_summary['Net_Profit'] = category_summary['Gross_Profit'] - category_summary['Sales_Commission'] - category_summary['Sales_Program']
category_summary['Net_Margin'] = (category_summary['Net_Profit']/category_summary['Revenue']*100).fillna(0)
col1,col2 = st.columns(2)
with col1:
fig_cat_revenue = px.bar(category_summary, x='Kategori', y='Revenue',
title="Revenue per Kategori", color='Revenue', color_continuous_scale='Blues')
fig_cat_revenue.update_layout(height=400)
st.plotly_chart(fig_cat_revenue, use_container_width=True)
with col2:
fig_cat_margin = px.bar(category_summary, x='Kategori', y='Net_Margin',
title="Net Margin per Kategori (%)", color='Net_Margin', color_continuous_scale='RdYlGn')
fig_cat_margin.update_layout(height=400)
st.plotly_chart(fig_cat_margin, use_container_width=True)
st.markdown("#### 📋 Ringkasan per Kategori")
display_data = category_summary.copy()
for col in ['Revenue','COGS','Sales_Commission','Sales_Program','Gross_Profit','Net_Profit']:
display_data[col] = display_data[col].apply(lambda x: f"Rp {x:,.0f}")
display_data['Net_Margin'] = display_data['Net_Margin'].apply(lambda x: f"{x:.2f}%")
st.dataframe(display_data, use_container_width=True)

def render_customer_analysis(df):
st.markdown("#### 👥 Analisis per Customer")
customer_summary = df.groupby('Nama_Customer').agg({
'Revenue':'sum','COGS':'sum','Sales_Commission':'sum','Sales_Program':'sum'
}).reset_index()
customer_summary['Gross_Profit'] = customer_summary['Revenue'] - customer_summary['COGS']
customer_summary['Net_Profit'] = customer_summary['Gross_Profit'] - customer_summary['Sales_Commission'] - customer_summary['Sales_Program']
customer_summary['Net_Margin'] = (customer_summary['Net_Profit']/customer_summary['Revenue']*100).fillna(0)
customer_summary = customer_summary.sort_values('Revenue',ascending=False)
col1,col2 = st.columns(2)
with col1:
top_customers = customer_summary.head(10)
fig_cust_revenue = px.bar(top_customers, x='Revenue', y='Nama_Customer',
title="Top 10 Revenue per Customer", color='Revenue',
color_continuous_scale='Blues', orientation='h')
fig_cust_revenue.update_layout(height=500)
st.plotly_chart(fig_cust_revenue, use_container_width=True)
with col2:
fig_cust_profit = px.bar(top_customers, x='Net_Profit', y='Nama_Customer',
title="Top 10 Net Profit per Customer", color='Net_Profit',
color_continuous_scale='RdYlGn', orientation='h')
fig_cust_profit.update_layout(height=500)
st.plotly_chart(fig_cust_profit, use_container_width=True)
st.markdown("#### 📊 Metrik Performa Customer")
col1,col2,col3 = st.columns(3)
with col1:
st.metric(label="👥 Total Customer", value=f"{len(customer_summary):,}")
with col2:
avg_revenue = customer_summary['Revenue'].mean()
st.metric(label="💰 Rata-rata Revenue per Customer", value=f"Rp {avg_revenue:,.0f}")
with col3:
if not customer_summary.empty:
st.metric(label="🏆 Customer Terbaik", value=customer_summary.iloc[0]['Nama_Customer'])
st.markdown("#### 📋 Ringkasan Top 15 Customer")
display_customer_data = customer_summary.head(15).copy()
for col in ['Revenue','COGS','Sales_Commission','Sales_Program','Gross_Profit','Net_Profit']:
display_customer_data[col] = display_customer_data[col].apply(lambda x: f"Rp {x:,.0f}")
display_customer_data['Net_Margin'] = display_customer_data['Net_Margin'].apply(lambda x: f"{x:.2f}%")
st.dataframe(display_customer_data, use_container_width=True)
st.markdown("#### 🥧 Kontribusi Revenue Customer (Top 10)")
fig_pie_customer = px.pie(customer_summary.head(10), values='Revenue', names='Nama_Customer',
title="Distribusi Revenue per Customer", color_discrete_sequence=px.colors.qualitative.Set3)
fig_pie_customer.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_pie_customer, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_customer_metrics(df, metrics):
    """Render customer-specific metrics and analysis"""
    if df.empty or 'Nama_Customer' not in df.columns:
        return
    
    st.subheader("👥 Analisis Customer")
    
    # Customer performance summary
    customer_metrics = calculate_customer_metrics(df)
    
    if customer_metrics.empty:
        st.info("💡 Tidak ada data customer untuk ditampilkan.")
        return
    
    # Top customer metrics
    display_top_customers(customer_metrics)
    
    # Customer trends over time
    display_customer_trends(df)
    
    # Customer profitability analysis
    display_customer_profitability(customer_metrics)

def calculate_customer_metrics(df):
    """Calculate metrics grouped by customer"""
    customer_metrics = df.groupby('Nama_Customer').agg({
        'Revenue': ['sum', 'count', 'mean'],
        'COGS': 'sum',
        'Sales_Commission': 'sum',
        'Sales_Program': 'sum',
        'Tanggal': ['min', 'max']
    }).round(2)
    
    # Flatten column names
    customer_metrics.columns = ['Total_Revenue', 'Jumlah_Transaksi', 'Avg_Revenue', 
                               'Total_COGS', 'Total_Sales_Commission', 'Total_Sales_Program',
                               'First_Transaction', 'Last_Transaction']
    
    # Calculate derived metrics
    customer_metrics['Gross_Profit'] = customer_metrics['Total_Revenue'] - customer_metrics['Total_COGS']
    customer_metrics['Total_Expenses'] = customer_metrics['Total_Sales_Commission'] + customer_metrics['Total_Sales_Program']
    customer_metrics['Net_Profit'] = customer_metrics['Gross_Profit'] - customer_metrics['Total_Expenses']
    customer_metrics['Net_Margin'] = (customer_metrics['Net_Profit'] / customer_metrics['Total_Revenue'] * 100).fillna(0)
    customer_metrics['Days_Active'] = (customer_metrics['Last_Transaction'] - customer_metrics['First_Transaction']).dt.days + 1
    
    # Reset index to make customer name a column
    customer_metrics = customer_metrics.reset_index()
    
    # Sort by total revenue
    customer_metrics = customer_metrics.sort_values('Total_Revenue', ascending=False)
    
    return customer_metrics

def display_top_customers(customer_metrics):
    """Display top customer metrics"""
    st.markdown("#### 🏆 Top Customer Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Top revenue customer
        top_revenue = customer_metrics.iloc[0] if not customer_metrics.empty else None
        if top_revenue is not None:
            st.metric(
                label="💰 Highest Revenue",
                value=top_revenue['Nama_Customer'],
                delta=f"Rp {top_revenue['Total_Revenue']:,.0f}"
            )
    
    with col2:
        # Most profitable customer
        most_profitable = customer_metrics.loc[customer_metrics['Net_Profit'].idxmax()] if not customer_metrics.empty else None
        if most_profitable is not None:
            st.metric(
                label="🎯 Most Profitable",
                value=most_profitable['Nama_Customer'],
                delta=f"Rp {most_profitable['Net_Profit']:,.0f}"
            )
    
    with col3:
        # Most frequent customer
        most_frequent = customer_metrics.loc[customer_metrics['Jumlah_Transaksi'].idxmax()] if not customer_metrics.empty else None
        if most_frequent is not None:
            st.metric(
                label="🔄 Most Transactions",
                value=most_frequent['Nama_Customer'],
                delta=f"{most_frequent['Jumlah_Transaksi']:,.0f} transaksi"
            )
    
    with col4:
        # Best margin customer
        best_margin = customer_metrics.loc[customer_metrics['Net_Margin'].idxmax()] if not customer_metrics.empty else None
        if best_margin is not None:
            st.metric(
                label="📈 Best Margin",
                value=best_margin['Nama_Customer'],
                delta=f"{best_margin['Net_Margin']:.2f}%"
            )

def display_customer_trends(df):
    """Display customer trends over time"""
    st.markdown("#### 📈 Tren Customer dari Waktu ke Waktu")
    
    # Monthly customer revenue trends (top 5 customers)
    monthly_customer = df.copy()
    monthly_customer['Year_Month'] = monthly_customer['Tanggal'].dt.to_period('M')
    
    # Get top 5 customers by total revenue
    top5_customers = df.groupby('Nama_Customer')['Revenue'].sum().nlargest(5).index.tolist()
    
    # Filter for top 5 customers
    monthly_customer_filtered = monthly_customer[monthly_customer['Nama_Customer'].isin(top5_customers)]
    
    monthly_trends = monthly_customer_filtered.groupby(['Year_Month', 'Nama_Customer'])['Revenue'].sum().reset_index()
    monthly_trends['Month'] = monthly_trends['Year_Month'].astype(str)
    
    if not monthly_trends.empty:
        fig_trends = px.line(
            monthly_trends,
            x='Month',
            y='Revenue',
            color='Nama_Customer',
            title="Tren Revenue Bulanan (Top 5 Customer)",
            markers=True
        )
        
        fig_trends.update_layout(
            xaxis_title="Bulan",
            yaxis_title="Revenue (Rp)",
            height=400
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)

def display_customer_profitability(customer_metrics):
    """Display customer profitability analysis"""
    st.markdown("#### 💹 Analisis Profitabilitas Customer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue vs Profit scatter plot (top 20 customers)
        top20 = customer_metrics.head(20)
        
        fig_scatter = px.scatter(
            top20,
            x='Total_Revenue',
            y='Net_Profit',
            size='Jumlah_Transaksi',
            hover_name='Nama_Customer',
            title="Revenue vs Net Profit (Top 20 Customer)",
            color='Net_Margin',
            color_continuous_scale='RdYlGn'
        )
        
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Customer segmentation based on revenue quartiles
        if len(customer_metrics) >= 4:
            customer_metrics['Revenue_Quartile'] = pd.qcut(
                customer_metrics['Total_Revenue'], 
                q=4, 
                labels=['Low', 'Medium-Low', 'Medium-High', 'High']
            )
            
            quartile_summary = customer_metrics.groupby('Revenue_Quartile').agg({
                'Nama_Customer': 'count',
                'Total_Revenue': 'sum',
                'Net_Profit': 'sum'
            }).reset_index()
            
            fig_segment = px.bar(
                quartile_summary,
                x='Revenue_Quartile',
                y='Nama_Customer',
                title="Segmentasi Customer berdasarkan Revenue",
                color='Revenue_Quartile',
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            fig_segment.update_layout(
                xaxis_title="Segmen Customer",
                yaxis_title="Jumlah Customer",
                height=400
            )
            
            st.plotly_chart(fig_segment, use_container_width=True)
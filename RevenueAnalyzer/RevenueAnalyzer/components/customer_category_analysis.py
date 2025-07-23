import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def render_customer_category_analysis(df):
    """Render analysis of customer behavior across different product categories"""
    if df.empty or 'Nama_Customer' not in df.columns or 'Kategori' not in df.columns:
        return
    
    st.subheader("🔍 Analisis Customer per Kategori Produk")
    
    # Customer-Category Matrix Analysis
    render_customer_category_matrix(df)
    
    # Category diversification analysis
    render_category_diversification(df)
    
    # Cross-category performance
    render_cross_category_performance(df)

def render_customer_category_matrix(df):
    """Display customer-category interaction matrix"""
    st.markdown("#### 📊 Matriks Customer vs Kategori")
    
    # Create pivot table for customer-category analysis
    customer_category_matrix = df.groupby(['Nama_Customer', 'Kategori']).agg({
        'Revenue': 'sum',
        'COGS': 'sum',
        'Sales_Commission': 'sum',
        'Sales_Program': 'sum'
    }).reset_index()
    
    customer_category_matrix['Net_Profit'] = (
        customer_category_matrix['Revenue'] - 
        customer_category_matrix['COGS'] - 
        customer_category_matrix['Sales_Commission'] - 
        customer_category_matrix['Sales_Program']
    )
    
    # Get top customers for better visualization
    top_customers = df.groupby('Nama_Customer')['Revenue'].sum().nlargest(10).index.tolist()
    matrix_filtered = customer_category_matrix[
        customer_category_matrix['Nama_Customer'].isin(top_customers)
    ]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue heatmap
        revenue_pivot = matrix_filtered.pivot(
            index='Nama_Customer', 
            columns='Kategori', 
            values='Revenue'
        ).fillna(0)
        
        if not revenue_pivot.empty:
            fig_heatmap = px.imshow(
                revenue_pivot,
                title="Revenue per Customer-Kategori (Top 10 Customer)",
                color_continuous_scale="Blues",
                aspect="auto"
            )
            fig_heatmap.update_layout(height=400)
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        # Profit margin heatmap
        profit_pivot = matrix_filtered.pivot(
            index='Nama_Customer', 
            columns='Kategori', 
            values='Net_Profit'
        ).fillna(0)
        
        if not profit_pivot.empty:
            # Calculate margin percentage
            revenue_pivot_for_margin = matrix_filtered.pivot(
                index='Nama_Customer', 
                columns='Kategori', 
                values='Revenue'
            ).fillna(0)
            
            margin_pivot = (profit_pivot / revenue_pivot_for_margin * 100).fillna(0)
            
            fig_margin_heatmap = px.imshow(
                margin_pivot,
                title="Net Margin (%) per Customer-Kategori",
                color_continuous_scale="RdYlGn",
                aspect="auto"
            )
            fig_margin_heatmap.update_layout(height=400)
            st.plotly_chart(fig_margin_heatmap, use_container_width=True)

def render_category_diversification(df):
    """Analyze how diversified each customer is across categories"""
    st.markdown("#### 🌈 Diversifikasi Kategori per Customer")
    
    # Calculate category count per customer
    customer_diversification = df.groupby('Nama_Customer').agg({
        'Kategori': 'nunique',
        'Revenue': 'sum'
    }).reset_index()
    
    customer_diversification.columns = ['Nama_Customer', 'Jumlah_Kategori', 'Total_Revenue']
    customer_diversification = customer_diversification.sort_values('Total_Revenue', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Scatter plot: Revenue vs Category Diversity
        fig_scatter = px.scatter(
            customer_diversification.head(20),
            x='Jumlah_Kategori',
            y='Total_Revenue',
            size='Total_Revenue',
            hover_name='Nama_Customer',
            title="Revenue vs Diversitas Kategori (Top 20 Customer)",
            color='Jumlah_Kategori',
            color_continuous_scale='Viridis'
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Distribution of category diversity
        diversity_dist = customer_diversification['Jumlah_Kategori'].value_counts().reset_index()
        diversity_dist.columns = ['Jumlah_Kategori', 'Jumlah_Customer']
        
        fig_bar = px.bar(
            diversity_dist,
            x='Jumlah_Kategori',
            y='Jumlah_Customer',
            title="Distribusi Diversitas Kategori",
            color='Jumlah_Customer',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=400)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Summary metrics
    st.markdown("#### 📈 Metrik Diversifikasi")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_categories = customer_diversification['Jumlah_Kategori'].mean()
        st.metric(
            label="🎯 Rata-rata Kategori per Customer",
            value=f"{avg_categories:.1f}"
        )
    
    with col2:
        most_diverse = customer_diversification.loc[
            customer_diversification['Jumlah_Kategori'].idxmax()
        ]
        st.metric(
            label="🌟 Customer Paling Diversifikasi",
            value=most_diverse['Nama_Customer'],
            delta=f"{most_diverse['Jumlah_Kategori']} kategori"
        )
    
    with col3:
        single_category_customers = len(
            customer_diversification[customer_diversification['Jumlah_Kategori'] == 1]
        )
        total_customers = len(customer_diversification)
        single_category_pct = (single_category_customers / total_customers * 100) if total_customers > 0 else 0
        
        st.metric(
            label="📍 Customer Satu Kategori",
            value=f"{single_category_customers}",
            delta=f"{single_category_pct:.1f}% dari total"
        )
    
    with col4:
        multi_category_revenue = customer_diversification[
            customer_diversification['Jumlah_Kategori'] > 1
        ]['Total_Revenue'].sum()
        total_revenue = customer_diversification['Total_Revenue'].sum()
        multi_category_pct = (multi_category_revenue / total_revenue * 100) if total_revenue > 0 else 0
        
        st.metric(
            label="💰 Revenue dari Multi-Kategori",
            value=f"{multi_category_pct:.1f}%",
            delta=f"Rp {multi_category_revenue:,.0f}"
        )

def render_cross_category_performance(df):
    """Analyze performance across different category combinations"""
    st.markdown("#### 🔄 Performa Cross-Category")
    
    # Find customers with multiple categories
    multi_category_customers = df.groupby('Nama_Customer')['Kategori'].nunique()
    multi_category_customers = multi_category_customers[multi_category_customers > 1].index.tolist()
    
    if not multi_category_customers:
        st.info("💡 Belum ada customer yang membeli dari multiple kategori.")
        return
    
    # Analyze performance for multi-category customers
    multi_cat_df = df[df['Nama_Customer'].isin(multi_category_customers)]
    
    # Category performance comparison for multi-category customers
    category_performance = multi_cat_df.groupby(['Nama_Customer', 'Kategori']).agg({
        'Revenue': 'sum',
        'COGS': 'sum',
        'Sales_Commission': 'sum',
        'Sales_Program': 'sum'
    }).reset_index()
    
    category_performance['Net_Profit'] = (
        category_performance['Revenue'] - 
        category_performance['COGS'] - 
        category_performance['Sales_Commission'] - 
        category_performance['Sales_Program']
    )
    
    category_performance['Net_Margin'] = (
        category_performance['Net_Profit'] / 
        category_performance['Revenue'] * 100
    ).fillna(0)
    
    # Top 5 multi-category customers
    top_multi_customers = df[df['Nama_Customer'].isin(multi_category_customers)].groupby(
        'Nama_Customer'
    )['Revenue'].sum().nlargest(5).index.tolist()
    
    if top_multi_customers:
        # Stacked bar chart for top multi-category customers
        top_multi_performance = category_performance[
            category_performance['Nama_Customer'].isin(top_multi_customers)
        ]
        
        fig_stacked = px.bar(
            top_multi_performance,
            x='Nama_Customer',
            y='Revenue',
            color='Kategori',
            title="Revenue per Kategori - Top 5 Multi-Category Customer",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_stacked.update_layout(height=400)
        st.plotly_chart(fig_stacked, use_container_width=True)
        
        # Category contribution table for multi-category customers
        st.markdown("#### 📋 Detail Multi-Category Customer")
        
        # Calculate category contribution percentage
        customer_totals = category_performance.groupby('Nama_Customer')['Revenue'].sum().to_dict()
        category_performance['Contribution_Pct'] = category_performance.apply(
            lambda row: (row['Revenue'] / customer_totals[row['Nama_Customer']] * 100), 
            axis=1
        )
        
        # Filter and format for display
        display_multi_cat = top_multi_performance.copy()
        display_multi_cat['Revenue_Formatted'] = display_multi_cat['Revenue'].apply(
            lambda x: f"Rp {x:,.0f}"
        )
        display_multi_cat['Net_Profit_Formatted'] = display_multi_cat['Net_Profit'].apply(
            lambda x: f"Rp {x:,.0f}"
        )
        display_multi_cat['Net_Margin_Formatted'] = display_multi_cat['Net_Margin'].apply(
            lambda x: f"{x:.2f}%"
        )
        
        # Add contribution percentage
        display_multi_cat['Contribution_Pct'] = display_multi_cat.apply(
            lambda row: (row['Revenue'] / customer_totals[row['Nama_Customer']] * 100), 
            axis=1
        )
        display_multi_cat['Contribution_Formatted'] = display_multi_cat['Contribution_Pct'].apply(
            lambda x: f"{x:.1f}%"
        )
        
        # Select columns for display
        display_columns = [
            'Nama_Customer', 'Kategori', 'Revenue_Formatted', 
            'Net_Profit_Formatted', 'Net_Margin_Formatted', 'Contribution_Formatted'
        ]
        
        display_multi_cat_final = display_multi_cat[display_columns].copy()
        display_multi_cat_final.columns = [
            'Customer', 'Kategori', 'Revenue', 'Net Profit', 
            'Net Margin', 'Kontribusi (%)'
        ]
        
        st.dataframe(display_multi_cat_final, use_container_width=True)
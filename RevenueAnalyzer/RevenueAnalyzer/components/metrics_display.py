import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def render_metrics(metrics, calculator):
    """Render key financial metrics display"""
    st.subheader("📈 Ringkasan Kinerja Keuangan")
    
    totals = metrics['totals']
    margins = metrics['margins']
    current_period = metrics['period_comparison']['current']
    previous_period = metrics['period_comparison']['previous']
    
    # Main metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        revenue_growth = ""
        if current_period and previous_period:
            growth = calculator.calculate_growth_rate(
                current_period['revenue'], 
                previous_period['revenue']
            )
            if growth > 0:
                revenue_growth = f" (+{growth:.1f}%)"
            elif growth < 0:
                revenue_growth = f" ({growth:.1f}%)"
        
        st.metric(
            label="💰 Total Revenue",
            value=f"Rp {totals['revenue']:,.0f}",
            delta=revenue_growth if revenue_growth else None
        )
    
    with col2:
        cogs_growth = ""
        if current_period and previous_period:
            growth = calculator.calculate_growth_rate(
                current_period['cogs'], 
                previous_period['cogs']
            )
            if growth > 0:
                cogs_growth = f" (+{growth:.1f}%)"
            elif growth < 0:
                cogs_growth = f" ({growth:.1f}%)"
        
        st.metric(
            label="📦 Total COGS",
            value=f"Rp {totals['cogs']:,.0f}",
            delta=cogs_growth if cogs_growth else None
        )
    
    with col3:
        st.metric(
            label="🎯 Komisi Penjualan",
            value=f"Rp {totals['sales_commission']:,.0f}"
        )
    
    with col4:
        st.metric(
            label="🎪 Program Penjualan",
            value=f"Rp {totals['sales_program']:,.0f}"
        )
    
    # Profit metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        profit_color = "normal"
        if totals['gross_profit'] < 0:
            profit_color = "inverse"
        
        st.metric(
            label="💵 Gross Profit",
            value=f"Rp {totals['gross_profit']:,.0f}",
            delta=None
        )
    
    with col2:
        net_profit_color = "normal"
        if totals['net_profit'] < 0:
            net_profit_color = "inverse"
        
        net_profit_growth = ""
        if current_period and previous_period:
            growth = calculator.calculate_growth_rate(
                current_period['net_profit'], 
                previous_period['net_profit']
            )
            if growth > 0:
                net_profit_growth = f" (+{growth:.1f}%)"
            elif growth < 0:
                net_profit_growth = f" ({growth:.1f}%)"
        
        st.metric(
            label="🏆 Net Profit",
            value=f"Rp {totals['net_profit']:,.0f}",
            delta=net_profit_growth if net_profit_growth else None
        )
    
    with col3:
        margin_color = "🟢" if margins['gross_margin'] > 0 else "🔴"
        st.metric(
            label=f"{margin_color} Gross Margin",
            value=f"{margins['gross_margin']:.2f}%"
        )
    
    with col4:
        net_margin_color = "🟢" if margins['net_margin'] > 0 else "🔴"
        st.metric(
            label=f"{net_margin_color} Net Margin",
            value=f"{margins['net_margin']:.2f}%"
        )
    
    # Expense breakdown
    st.markdown("---")
    st.subheader("💸 Breakdown Pengeluaran")
    
    # Create expense breakdown chart
    if totals['total_expenses'] > 0:
        expense_data = {
            'Kategori': ['COGS', 'Komisi Penjualan', 'Program Penjualan'],
            'Jumlah': [totals['cogs'], totals['sales_commission'], totals['sales_program']],
            'Persentase': [
                (totals['cogs'] / totals['revenue'] * 100) if totals['revenue'] > 0 else 0,
                (totals['sales_commission'] / totals['revenue'] * 100) if totals['revenue'] > 0 else 0,
                (totals['sales_program'] / totals['revenue'] * 100) if totals['revenue'] > 0 else 0
            ]
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie chart for expense breakdown
            fig_pie = px.pie(
                values=expense_data['Jumlah'],
                names=expense_data['Kategori'],
                title="Distribusi Pengeluaran",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Bar chart for expense amounts
            fig_bar = px.bar(
                x=expense_data['Kategori'],
                y=expense_data['Jumlah'],
                title="Jumlah Pengeluaran per Kategori",
                color=expense_data['Kategori'],
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_bar.update_layout(
                xaxis_title="Kategori",
                yaxis_title="Jumlah (Rp)",
                showlegend=False
            )
            fig_bar.update_traces(text=[f"Rp {val:,.0f}" for val in expense_data['Jumlah']], textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Expense percentage table
        st.markdown("#### 📊 Persentase terhadap Revenue")
        expense_df = {
            'Kategori Pengeluaran': expense_data['Kategori'],
            'Jumlah (Rp)': [f"Rp {val:,.0f}" for val in expense_data['Jumlah']],
            'Persentase dari Revenue': [f"{val:.2f}%" for val in expense_data['Persentase']]
        }
        st.table(expense_df)
    
    else:
        st.info("💡 Tidak ada data pengeluaran untuk ditampilkan.")

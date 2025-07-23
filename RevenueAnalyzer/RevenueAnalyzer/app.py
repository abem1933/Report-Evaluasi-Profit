import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from utils.data_processor import DataProcessor
from utils.calculations import FinancialCalculator
from components.sidebar import render_sidebar
from components.metrics_display import render_metrics
from components.charts import render_charts
from components.data_upload import render_data_upload
from components.customer_metrics import render_customer_metrics
from components.customer_category_analysis import render_customer_category_analysis
from components.database_management import render_database_management, render_data_source_selector

# Configure page
st.set_page_config(
    page_title="Dashboard Laporan Keuangan",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'financial_data' not in st.session_state:
    st.session_state.financial_data = None
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'data_source' not in st.session_state:
    st.session_state.data_source = 'database'

def main():
    st.title("📊 Dashboard Laporan Keuangan - Evaluasi Profit")
    st.markdown("---")
    
    # Initialize components
    data_processor = DataProcessor()
    calculator = FinancialCalculator()
    
    # Render sidebar
    filters = render_sidebar()
    
    # Render data source selector
    st.session_state.data_source = render_data_source_selector()
    
    # Handle data source selection
    if st.session_state.data_source == 'database':
        # Try to get data from database
        try:
            db_data = data_processor.get_data_from_database(filters)
            if not db_data.empty:
                st.session_state.processed_data = db_data
                st.session_state.data_loaded = True
            else:
                st.session_state.data_loaded = False
        except Exception as e:
            st.error(f"❌ Error loading data from database: {str(e)}")
            st.session_state.data_loaded = False
    
    # Show data upload and database management tabs
    if not st.session_state.data_loaded or st.session_state.data_source == 'upload':
        tab1, tab2 = st.tabs(["📁 Upload Data", "🗄️ Database Management"])
        
        with tab1:
            if not st.session_state.data_loaded:
                st.info("👆 Silakan unggah data keuangan Anda menggunakan sidebar di sebelah kiri untuk memulai analisis.")
            
            # Show data upload component
            uploaded_data = render_data_upload()
            
            if uploaded_data is not None:
                try:
                    # Process uploaded data
                    processed_data = data_processor.process_uploaded_data(uploaded_data)
                    st.session_state.financial_data = uploaded_data
                    st.session_state.processed_data = processed_data
                    st.session_state.data_loaded = True
                    st.success("✅ Data berhasil dimuat! Dashboard akan dimuat ulang...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error memproses data: {str(e)}")
            
            # Show example data structure
            if not st.session_state.data_loaded:
                st.markdown("### 📋 Format Data yang Diperlukan")
                st.markdown("""
                File CSV/Excel Anda harus memiliki kolom berikut:
                - **Tanggal**: Format tanggal (YYYY-MM-DD)
                - **Revenue**: Pendapatan
                - **COGS**: Harga Pokok Penjualan
                - **Sales_Commission**: Komisi Penjualan
                - **Sales_Program**: Program Penjualan
                - **Nama_Customer**: Nama Customer
                - **Kategori**: Kategori produk/layanan (opsional)
                """)
        
        with tab2:
            render_database_management()
        
        if not st.session_state.data_loaded:
            return
    
    # Process data with filters if data is loaded
    if st.session_state.processed_data is not None:
        try:
            # Get data based on source
            if st.session_state.data_source == 'database':
                # Get filtered data directly from database
                filtered_data = data_processor.get_data_from_database(filters)
            else:
                # Apply filters to session data
                filtered_data = data_processor.apply_filters(
                    st.session_state.processed_data, 
                    filters
                )
            
            if filtered_data is None or (hasattr(filtered_data, 'empty') and filtered_data.empty):
                st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
                return
            
            # Calculate financial metrics
            metrics = calculator.calculate_metrics(filtered_data)
            
            # Render metrics display
            render_metrics(metrics, calculator)
            
            st.markdown("---")
            
            # Render charts
            render_charts(filtered_data, metrics, calculator)
            
            st.markdown("---")
            
            # Render customer metrics if customer data exists
            if hasattr(filtered_data, 'columns') and 'Nama_Customer' in filtered_data.columns:
                render_customer_metrics(filtered_data, metrics)
                
                st.markdown("---")
                
                # Render customer-category analysis if both columns exist
                if hasattr(filtered_data, 'columns') and 'Kategori' in filtered_data.columns and len(filtered_data['Kategori'].unique()) > 1:
                    render_customer_category_analysis(filtered_data)
            
            # Export functionality
            st.markdown("---")
            st.subheader("📥 Ekspor Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Unduh Laporan Ringkasan"):
                    summary_data = calculator.generate_summary_report(filtered_data, metrics)
                    csv = summary_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"laporan_keuangan_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                if st.button("📈 Unduh Data Detail"):
                    if hasattr(filtered_data, 'to_csv'):
                        csv = filtered_data.to_csv(index=False)
                        st.download_button(
                            label="💾 Download CSV Detail",
                            data=csv,
                            file_name=f"data_detail_{datetime.now().strftime('%Y%m%d')}.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error("❌ Cannot export data: Invalid data format")
                    
        except Exception as e:
            st.error(f"❌ Error memproses data: {str(e)}")
            st.info("💡 Pastikan format data Anda sesuai dengan requirement yang ditentukan.")

if __name__ == "__main__":
    main()

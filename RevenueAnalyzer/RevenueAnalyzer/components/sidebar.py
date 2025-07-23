import streamlit as st
from datetime import datetime, timedelta
from utils.data_processor import DataProcessor

def render_sidebar():
    """Render sidebar with filters and data upload"""
    st.sidebar.title("🔧 Kontrol & Filter")
    
    data_processor = DataProcessor()
    
    # Data upload section
    st.sidebar.markdown("### 📁 Upload Data")
    uploaded_file = st.sidebar.file_uploader(
        "Pilih file CSV atau Excel",
        type=['csv', 'xlsx', 'xls'],
        help="File harus berisi kolom: Tanggal, Revenue, COGS, Sales_Commission, Sales_Program, Nama_Customer"
    )
    
    if uploaded_file:
        if st.sidebar.button("🔄 Proses Data Baru"):
            try:
                # Process new data
                processed_data = data_processor.process_uploaded_data(uploaded_file)
                st.session_state.financial_data = uploaded_file
                st.session_state.processed_data = processed_data
                st.session_state.data_loaded = True
                st.sidebar.success("✅ Data berhasil diperbarui!")
                st.rerun()
            except Exception as e:
                st.sidebar.error(f"❌ Error: {str(e)}")
    
    st.sidebar.markdown("---")
    
    # Filter section
    st.sidebar.markdown("### 🎯 Filter Data")
    
    # Initialize default filters
    filters = {
        'start_date': None,
        'end_date': None,
        'categories': ['Semua'],
        'customers': ['Semua']
    }
    
    # Only show filters if data is loaded
    if st.session_state.data_loaded or st.session_state.get('data_source') == 'database':
        # Get available options from database if using database source
        if st.session_state.get('data_source') == 'database':
            df = None  # We'll get data from database
        else:
            df = st.session_state.processed_data
        
        # Date range filter
        min_date, max_date = data_processor.get_date_range(df)
        
        if min_date and max_date:
            st.sidebar.markdown("#### 📅 Rentang Tanggal")
            
            # Default to last 30 days or full range if less than 30 days
            if (max_date - min_date).days > 30:
                default_start = max_date - timedelta(days=30)
            else:
                default_start = min_date
            
            start_date = st.sidebar.date_input(
                "Tanggal Mulai",
                value=default_start,
                min_value=min_date,
                max_value=max_date
            )
            
            end_date = st.sidebar.date_input(
                "Tanggal Akhir",
                value=max_date,
                min_value=min_date,
                max_value=max_date
            )
            
            if start_date > end_date:
                st.sidebar.error("⚠️ Tanggal mulai tidak boleh lebih besar dari tanggal akhir!")
                start_date = end_date
            
            filters['start_date'] = start_date
            filters['end_date'] = end_date
        
        # Category filter
        categories = data_processor.get_available_categories(df)
        if len(categories) > 1:  # More than just "Semua"
            st.sidebar.markdown("#### 🏷️ Kategori")
            selected_categories = st.sidebar.multiselect(
                "Pilih Kategori",
                options=categories,
                default=['Semua']
            )
            filters['categories'] = selected_categories
        
        # Customer filter
        customers = data_processor.get_available_customers(df)
        if len(customers) > 1:  # More than just "Semua"
            st.sidebar.markdown("#### 👥 Customer")
            selected_customers = st.sidebar.multiselect(
                "Pilih Customer",
                options=customers,
                default=['Semua']
            )
            filters['customers'] = selected_customers
        
        # Quick filter buttons
        st.sidebar.markdown("#### ⚡ Filter Cepat")
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button("7 Hari") and max_date:
                filters['start_date'] = max_date - timedelta(days=7)
                filters['end_date'] = max_date
                st.rerun()
        
        with col2:
            if st.button("30 Hari") and max_date:
                filters['start_date'] = max_date - timedelta(days=30)
                filters['end_date'] = max_date
                st.rerun()
        
        col3, col4 = st.sidebar.columns(2)
        
        with col3:
            if st.button("90 Hari") and max_date:
                filters['start_date'] = max_date - timedelta(days=90)
                filters['end_date'] = max_date
                st.rerun()
        
        with col4:
            if st.button("Semua"):
                filters['start_date'] = min_date
                filters['end_date'] = max_date
                st.rerun()
        
        # Data info
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📊 Info Data")
        customers = data_processor.get_available_customers(df)
        if min_date and max_date:
            record_count = len(df) if df is not None and hasattr(df, '__len__') else 0
            st.sidebar.info(f"""
            **Total Records**: {record_count:,}
            
            **Periode Data**: 
            {min_date.strftime('%d %b %Y')} - {max_date.strftime('%d %b %Y')}
            
            **Kategori**: {len(categories)-1 if categories else 0} kategori
            
            **Customer**: {len(customers)-1 if customers else 0} customer
            """)
        else:
            record_count = len(df) if df is not None and hasattr(df, '__len__') else 0
            st.sidebar.info(f"""
            **Total Records**: {record_count:,}
            
            **Kategori**: {len(categories)-1 if categories else 0} kategori
            
            **Customer**: {len(customers)-1 if customers else 0} customer
            """)
    
    else:
        st.sidebar.info("📤 Unggah data untuk menggunakan filter")
    
    return filters

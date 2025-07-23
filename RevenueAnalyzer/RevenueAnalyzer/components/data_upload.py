import streamlit as st
import pandas as pd
from io import StringIO

def render_data_upload():
    """Render data upload component with instructions"""
    st.markdown("### 📁 Upload Data Keuangan")
    
    # Instructions
    with st.expander("📖 Panduan Upload Data", expanded=True):
        st.markdown("""
        #### Format File yang Didukung:
        - **CSV** (.csv)
        - **Excel** (.xlsx, .xls)
        
        #### Kolom yang Diperlukan:
        | Nama Kolom | Deskripsi | Contoh |
        |------------|-----------|--------|
        | `Tanggal` | Tanggal transaksi (YYYY-MM-DD) | 2024-01-15 |
        | `Revenue` | Pendapatan | 1000000 |
        | `COGS` | Harga Pokok Penjualan | 600000 |
        | `Sales_Commission` | Komisi Penjualan | 50000 |
        | `Sales_Program` | Program Penjualan | 30000 |
        | `Nama_Customer` | Nama Customer | PT. ABC Corp |
        | `Kategori` | Kategori produk (opsional) | Elektronik |
        
        #### Tips:
        - 💡 Pastikan format tanggal konsisten
        - 💡 Gunakan angka tanpa simbol mata uang
        - 💡 Nama Customer wajib diisi untuk analisis per customer
        - 💡 Satu customer bisa memiliki beberapa kategori produk
        - 💡 Kolom Kategori bersifat opsional
        - 💡 Data akan divalidasi setelah upload
        """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Pilih file data keuangan Anda",
        type=['csv', 'xlsx', 'xls'],
        help="Upload file CSV atau Excel dengan format yang sesuai"
    )
    
    if uploaded_file is not None:
        # Show file info
        st.success(f"✅ File berhasil dipilih: **{uploaded_file.name}**")
        
        # Preview data
        with st.expander("👀 Preview Data"):
            try:
                # Read first few rows for preview
                if uploaded_file.name.endswith('.csv'):
                    preview_df = pd.read_csv(uploaded_file, nrows=5)
                else:
                    preview_df = pd.read_excel(uploaded_file, nrows=5)
                
                st.dataframe(preview_df, use_container_width=True)
                
                # Show data info
                st.info(f"""
                **Info Preview:**
                - Jumlah kolom: {len(preview_df.columns)}
                - Kolom yang tersedia: {', '.join(preview_df.columns.tolist())}
                - Preview menampilkan 5 baris pertama
                """)
                
                # Reset file pointer
                uploaded_file.seek(0)
                
            except Exception as e:
                st.error(f"❌ Error membaca file: {str(e)}")
                return None
        
        return uploaded_file
    
    # Show sample data format
    st.markdown("---")
    st.markdown("### 📋 Contoh Format Data")
    
    # Create sample data
    sample_data = {
        'Tanggal': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'Revenue': [1000000, 1500000, 800000, 1200000, 900000],
        'COGS': [600000, 900000, 480000, 720000, 540000],
        'Sales_Commission': [50000, 75000, 40000, 60000, 45000],
        'Sales_Program': [30000, 45000, 25000, 35000, 30000],
        'Nama_Customer': ['PT. ABC Corp', 'CV. XYZ Ltd', 'PT. ABC Corp', 'PT. ABC Corp', 'CV. XYZ Ltd'],
        'Kategori': ['Elektronik', 'Fashion', 'Furniture', 'Elektronik', 'Elektronik']
    }
    
    sample_df = pd.DataFrame(sample_data)
    st.dataframe(sample_df, use_container_width=True)
    
    # Download sample template
    if st.button("📥 Download Template Excel"):
        # Create Excel file in memory
        from io import BytesIO
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            sample_df.to_excel(writer, sheet_name='Template Data', index=False)
        output.seek(0)
        
        st.download_button(
            label="💾 Download Template",
            data=output.getvalue(),
            file_name="template_data_keuangan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    return None

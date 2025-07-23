import streamlit as st
import pandas as pd
from database.database_manager import DatabaseManager

def render_database_management():
    """Render database management interface"""
    st.subheader("🗄️ Database Management")
    
    db_manager = DatabaseManager()
    
    # Database statistics
    st.markdown("#### 📊 Database Statistics")
    stats = db_manager.get_database_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📝 Total Records",
            value=f"{stats['total_records']:,}"
        )
    
    with col2:
        st.metric(
            label="👥 Total Customers",
            value=f"{stats['total_customers']:,}"
        )
    
    with col3:
        st.metric(
            label="🏷️ Total Categories",
            value=f"{stats['total_categories']:,}"
        )
    
    with col4:
        date_range = stats['date_range']
        if date_range['min_date'] and date_range['max_date']:
            days_span = (date_range['max_date'] - date_range['min_date']).days + 1
            st.metric(
                label="📅 Data Span",
                value=f"{days_span} days"
            )
        else:
            st.metric(
                label="📅 Data Span",
                value="No data"
            )
    
    # Upload history
    st.markdown("#### 📋 Recent Upload History")
    upload_history = db_manager.get_upload_history(limit=10)
    
    if not upload_history.empty:
        # Format the display
        display_history = upload_history.copy()
        display_history['upload_timestamp'] = pd.to_datetime(display_history['upload_timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
        display_history = display_history[['filename', 'records_count', 'status', 'upload_timestamp']]
        display_history.columns = ['Filename', 'Records', 'Status', 'Upload Time']
        
        st.dataframe(display_history, use_container_width=True)
    else:
        st.info("💡 No upload history available.")
    
    # Database actions
    st.markdown("#### ⚙️ Database Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Database Stats", help="Refresh the database statistics display"):
            st.rerun()
    
    with col2:
        if st.button("⬇️ Export All Data", help="Export all database data to CSV"):
            try:
                all_data = db_manager.get_financial_data()
                if not all_data.empty:
                    csv = all_data.to_csv(index=False)
                    st.download_button(
                        label="💾 Download CSV",
                        data=csv,
                        file_name=f"financial_data_export_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No data available to export.")
            except Exception as e:
                st.error(f"❌ Error exporting data: {str(e)}")
    
    # Advanced actions (with warnings)
    st.markdown("#### ⚠️ Advanced Actions")
    st.warning("**Caution**: These actions cannot be undone!")
    
    if st.checkbox("Enable Advanced Actions"):
        if st.button("🗑️ Clear All Data", help="Delete all financial transaction data"):
            if st.checkbox("I understand this will delete ALL data"):
                try:
                    deleted_count = db_manager.clear_all_data()
                    st.success(f"✅ Deleted {deleted_count} records from database.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error clearing data: {str(e)}")

def render_data_source_selector():
    """Render data source selection"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🗄️ Data Source")
    
    data_source = st.sidebar.radio(
        "Select Data Source",
        options=["Database", "Upload Only"],
        help="Choose whether to load data from database or just from current upload"
    )
    
    if data_source == "Database":
        st.sidebar.info("📊 Using data from database")
        return "database"
    else:
        st.sidebar.info("📤 Using uploaded data only")
        return "upload"
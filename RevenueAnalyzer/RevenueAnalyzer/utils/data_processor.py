import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
import numpy as np
from database.database_manager import DatabaseManager

class DataProcessor:
    def __init__(self):
        self.required_columns = ['Tanggal', 'Revenue', 'COGS', 'Sales_Commission', 'Sales_Program', 'Nama_Customer']
        self.db_manager = DatabaseManager()
        
    def process_uploaded_data(self, uploaded_file):
        """Process uploaded CSV or Excel file"""
        try:
            # Read file based on extension
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                raise ValueError("Format file tidak didukung. Gunakan CSV atau Excel.")
            
            # Validate required columns
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Kolom yang hilang: {', '.join(missing_columns)}")
            
            # Convert date column
            df['Tanggal'] = pd.to_datetime(df['Tanggal'], errors='coerce')
            
            # Remove rows with invalid dates
            df = df.dropna(subset=['Tanggal'])
            
            if df.empty:
                raise ValueError("Tidak ada data valid setelah pemrosesan tanggal.")
            
            # Convert numeric columns
            numeric_columns = ['Revenue', 'COGS', 'Sales_Commission', 'Sales_Program']
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Remove rows with all NaN numeric values
            df = df.dropna(subset=numeric_columns, how='all')
            
            # Fill remaining NaN values with 0
            df[numeric_columns] = df[numeric_columns].fillna(0)
            
            # Add category column if not exists
            if 'Kategori' not in df.columns:
                df['Kategori'] = 'Umum'
            
            # Add customer name column if not exists
            if 'Nama_Customer' not in df.columns:
                df['Nama_Customer'] = 'Unknown Customer'
            
            # Sort by date
            df = df.sort_values('Tanggal').reset_index(drop=True)
            
            # Save to database
            try:
                records_saved = self.db_manager.save_financial_data(df, uploaded_file.name if hasattr(uploaded_file, 'name') else None)
                st.success(f"✅ Data berhasil disimpan ke database: {records_saved} records")
            except Exception as e:
                st.warning(f"⚠️ Data diproses tapi gagal disimpan ke database: {str(e)}")
            
            return df
            
        except Exception as e:
            raise Exception(f"Error memproses file: {str(e)}")
    
    def apply_filters(self, df, filters):
        """Apply date and category filters to the dataframe"""
        filtered_df = df.copy()
        
        # Apply date filter
        if filters['start_date'] and filters['end_date']:
            filtered_df = filtered_df[
                (filtered_df['Tanggal'] >= pd.Timestamp(filters['start_date'])) &
                (filtered_df['Tanggal'] <= pd.Timestamp(filters['end_date']))
            ]
        
        # Apply category filter
        if filters['categories'] and 'Semua' not in filters['categories']:
            filtered_df = filtered_df[filtered_df['Kategori'].isin(filters['categories'])]
        
        # Apply customer filter
        if filters['customers'] and 'Semua' not in filters['customers']:
            filtered_df = filtered_df[filtered_df['Nama_Customer'].isin(filters['customers'])]
        
        return filtered_df
    
    def get_available_categories(self, df=None):
        """Get list of available categories from database or dataframe"""
        try:
            return self.db_manager.get_available_categories()
        except:
            # Fallback to dataframe if database fails
            if df is None or df.empty:
                return ['Semua']
            categories = ['Semua'] + sorted(df['Kategori'].unique().tolist())
            return categories
    
    def get_available_customers(self, df=None):
        """Get list of available customers from database or dataframe"""
        try:
            return self.db_manager.get_available_customers()
        except:
            # Fallback to dataframe if database fails
            if df is None or df.empty:
                return ['Semua']
            customers = ['Semua'] + sorted(df['Nama_Customer'].unique().tolist())
            return customers
    
    def get_date_range(self, df=None):
        """Get the date range from database or dataframe"""
        try:
            return self.db_manager.get_date_range()
        except:
            # Fallback to dataframe if database fails
            if df is None or df.empty:
                return None, None
                
            min_date = df['Tanggal'].min().date()
            max_date = df['Tanggal'].max().date()
            
            return min_date, max_date
    
    def get_data_from_database(self, filters):
        """Get filtered data from database"""
        try:
            return self.db_manager.get_financial_data(
                start_date=filters.get('start_date'),
                end_date=filters.get('end_date'),
                customers=filters.get('customers'),
                categories=filters.get('categories')
            )
        except Exception as e:
            st.error(f"Error getting data from database: {str(e)}")
            return pd.DataFrame()

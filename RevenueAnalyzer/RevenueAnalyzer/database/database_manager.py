import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from database.models import FinancialTransaction, DataUploadLog, get_session, create_tables
from datetime import datetime
import streamlit as st

class DatabaseManager:
    """Manages database operations for financial data"""
    
    def __init__(self):
        self.ensure_tables_exist()
    
    def ensure_tables_exist(self):
        """Ensure database tables exist"""
        try:
            create_tables()
        except Exception as e:
            st.error(f"Error creating database tables: {str(e)}")
    
    def save_financial_data(self, df, filename=None):
        """Save financial data DataFrame to database"""
        session = get_session()
        try:
            # Clear existing data (you might want to modify this behavior)
            # session.query(FinancialTransaction).delete()
            
            records_added = 0
            for _, row in df.iterrows():
                transaction = FinancialTransaction(
                    tanggal=pd.to_datetime(row['Tanggal']),
                    revenue=float(row.get('Revenue', 0)),
                    cogs=float(row.get('COGS', 0)),
                    sales_commission=float(row.get('Sales_Commission', 0)),
                    sales_program=float(row.get('Sales_Program', 0)),
                    nama_customer=str(row.get('Nama_Customer', 'Unknown')),
                    kategori=str(row.get('Kategori', 'Umum'))
                )
                session.add(transaction)
                records_added += 1
            
            session.commit()
            
            # Log the upload
            if filename:
                self.log_data_upload(filename, records_added, 'success')
            
            return records_added
            
        except Exception as e:
            session.rollback()
            if filename:
                self.log_data_upload(filename, 0, 'error', str(e))
            raise e
        finally:
            session.close()
    
    def get_financial_data(self, start_date=None, end_date=None, customers=None, categories=None):
        """Retrieve financial data from database with filters"""
        session = get_session()
        try:
            query = session.query(FinancialTransaction)
            
            # Apply date filters
            if start_date:
                query = query.filter(FinancialTransaction.tanggal >= start_date)
            if end_date:
                query = query.filter(FinancialTransaction.tanggal <= end_date)
            
            # Apply customer filters
            if customers and 'Semua' not in customers:
                query = query.filter(FinancialTransaction.nama_customer.in_(customers))
            
            # Apply category filters
            if categories and 'Semua' not in categories:
                query = query.filter(FinancialTransaction.kategori.in_(categories))
            
            # Get results
            results = query.all()
            
            # Convert to DataFrame
            if results:
                data = [record.to_dict() for record in results]
                df = pd.DataFrame(data)
                return df
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"Error retrieving data from database: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def get_available_customers(self):
        """Get list of available customers from database"""
        session = get_session()
        try:
            result = session.query(FinancialTransaction.nama_customer).distinct().all()
            customers = ['Semua'] + [row[0] for row in result]
            return sorted(customers)
        except Exception as e:
            st.error(f"Error getting customers: {str(e)}")
            return ['Semua']
        finally:
            session.close()
    
    def get_available_categories(self):
        """Get list of available categories from database"""
        session = get_session()
        try:
            result = session.query(FinancialTransaction.kategori).distinct().all()
            categories = ['Semua'] + [row[0] for row in result if row[0]]
            return sorted(categories)
        except Exception as e:
            st.error(f"Error getting categories: {str(e)}")
            return ['Semua']
        finally:
            session.close()
    
    def get_date_range(self):
        """Get the date range of data in database"""
        session = get_session()
        try:
            result = session.query(
                FinancialTransaction.tanggal
            ).order_by(FinancialTransaction.tanggal.asc()).first()
            
            min_date = result[0].date() if result else None
            
            result = session.query(
                FinancialTransaction.tanggal
            ).order_by(FinancialTransaction.tanggal.desc()).first()
            
            max_date = result[0].date() if result else None
            
            return min_date, max_date
            
        except Exception as e:
            st.error(f"Error getting date range: {str(e)}")
            return None, None
        finally:
            session.close()
    
    def log_data_upload(self, filename, records_count, status='success', error_message=None):
        """Log data upload activity"""
        session = get_session()
        try:
            upload_log = DataUploadLog(
                filename=filename,
                records_count=records_count,
                status=status,
                error_message=error_message
            )
            session.add(upload_log)
            session.commit()
        except Exception as e:
            session.rollback()
            st.error(f"Error logging upload: {str(e)}")
        finally:
            session.close()
    
    def get_upload_history(self, limit=10):
        """Get recent upload history"""
        session = get_session()
        try:
            result = session.query(DataUploadLog).order_by(
                DataUploadLog.upload_timestamp.desc()
            ).limit(limit).all()
            
            if result:
                data = [log.to_dict() for log in result]
                return pd.DataFrame(data)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            st.error(f"Error getting upload history: {str(e)}")
            return pd.DataFrame()
        finally:
            session.close()
    
    def clear_all_data(self):
        """Clear all financial transaction data (use with caution)"""
        session = get_session()
        try:
            deleted_count = session.query(FinancialTransaction).delete()
            session.commit()
            return deleted_count
        except Exception as e:
            session.rollback()
            st.error(f"Error clearing data: {str(e)}")
            return 0
        finally:
            session.close()
    
    def get_database_stats(self):
        """Get database statistics"""
        session = get_session()
        try:
            total_records = session.query(FinancialTransaction).count()
            total_customers = session.query(FinancialTransaction.nama_customer).distinct().count()
            total_categories = session.query(FinancialTransaction.kategori).distinct().count()
            
            # Get date range
            min_date, max_date = self.get_date_range()
            
            return {
                'total_records': total_records,
                'total_customers': total_customers,
                'total_categories': total_categories,
                'date_range': {
                    'min_date': min_date,
                    'max_date': max_date
                }
            }
        except Exception as e:
            st.error(f"Error getting database stats: {str(e)}")
            return {
                'total_records': 0,
                'total_customers': 0,
                'total_categories': 0,
                'date_range': {'min_date': None, 'max_date': None}
            }
        finally:
            session.close()
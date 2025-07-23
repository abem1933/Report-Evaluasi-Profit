from sqlalchemy import Column, Integer, String, Float, DateTime, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class FinancialTransaction(Base):
    """Model for storing financial transaction data"""
    __tablename__ = 'financial_transactions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tanggal = Column(DateTime, nullable=False)
    revenue = Column(Float, nullable=False, default=0.0)
    cogs = Column(Float, nullable=False, default=0.0)
    sales_commission = Column(Float, nullable=False, default=0.0)
    sales_program = Column(Float, nullable=False, default=0.0)
    nama_customer = Column(String(255), nullable=False)
    kategori = Column(String(100), nullable=True, default='Umum')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'Tanggal': self.tanggal,
            'Revenue': self.revenue,
            'COGS': self.cogs,
            'Sales_Commission': self.sales_commission,
            'Sales_Program': self.sales_program,
            'Nama_Customer': self.nama_customer,
            'Kategori': self.kategori,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class DataUploadLog(Base):
    """Model for tracking data uploads"""
    __tablename__ = 'data_upload_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    records_count = Column(Integer, nullable=False)
    upload_timestamp = Column(DateTime, default=datetime.utcnow)
    file_size = Column(Integer, nullable=True)
    status = Column(String(50), nullable=False, default='success')
    error_message = Column(Text, nullable=True)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'filename': self.filename,
            'records_count': self.records_count,
            'upload_timestamp': self.upload_timestamp,
            'file_size': self.file_size,
            'status': self.status,
            'error_message': self.error_message
        }

# Database connection setup
def get_database_url():
    """Get database URL from environment variable"""
    return os.getenv('DATABASE_URL')

def create_database_engine():
    """Create SQLAlchemy engine"""
    database_url = get_database_url()
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    
    engine = create_engine(database_url, echo=False)
    return engine

def create_tables():
    """Create all tables in the database"""
    engine = create_database_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    """Get database session"""
    engine = create_database_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
# Financial Dashboard - Replit Configuration

## Overview

This is a Streamlit-based financial reporting dashboard built in Python that allows users to upload financial data and analyze profit metrics through interactive visualizations and calculations. The application processes CSV/Excel files containing financial transaction data and provides comprehensive profit analysis with charts, metrics, and trends. **Updated July 2025**: Added customer analysis functionality to track performance by individual customers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **Layout**: Wide layout with sidebar navigation and expandable main content area
- **Components**: Modular component-based architecture with separate files for different UI sections
- **Visualization**: Plotly for interactive charts and graphs
- **Styling**: Built-in Streamlit components with custom metrics displays

### Backend Architecture
- **Language**: Python 3.x
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Structure**: Utility-based architecture with separate modules for data processing and financial calculations
- **Session Management**: Streamlit session state with optional database persistence
- **Data Processing Pipeline**: Upload → Validation → Processing → Database Storage → Calculation → Visualization
- **Database Layer**: Complete CRUD operations with filtering and data management capabilities

### Data Processing Flow
1. **Data Upload**: CSV/Excel file upload through Streamlit file uploader
2. **Validation**: Check for required columns and data format validation
3. **Data Cleaning**: Date parsing, numeric conversion, and NaN handling
4. **Calculation**: Financial metrics computation including profit margins and growth rates
5. **Aggregation**: Monthly and period-based data grouping for trend analysis

## Key Components

### Core Modules
- **app.py**: Main application entry point with page configuration and flow orchestration
- **utils/data_processor.py**: DataProcessor class handling file upload, validation, data cleaning, and database integration
- **utils/calculations.py**: FinancialCalculator class for computing financial metrics and trends
- **database/models.py**: SQLAlchemy models for FinancialTransaction and DataUploadLog
- **database/database_manager.py**: DatabaseManager class for all database operations and queries

### UI Components
- **components/sidebar.py**: Sidebar rendering with upload controls and data filters (including customer filter)
- **components/data_upload.py**: Dedicated data upload interface with instructions and validation
- **components/metrics_display.py**: Financial metrics visualization with key performance indicators
- **components/charts.py**: Chart rendering for trends, profit analysis, category and customer breakdowns
- **components/customer_metrics.py**: Customer-specific analytics including performance metrics, trends, and profitability analysis
- **components/customer_category_analysis.py**: Multi-dimensional analysis of customer behavior across product categories with diversification metrics
- **components/database_management.py**: Database management interface with statistics, upload history, and data operations

### Required Data Schema
```
Tanggal: datetime (transaction date)
Revenue: numeric (revenue amount)
COGS: numeric (cost of goods sold)
Sales_Commission: numeric (sales commission expenses)
Sales_Program: numeric (sales program expenses)
Nama_Customer: string (customer name)
Kategori: string (optional product category)
```

## Data Flow

1. **Upload Phase**: User uploads CSV/Excel file through sidebar or main upload component
2. **Processing Phase**: DataProcessor validates columns, converts data types, and cleans invalid entries
3. **Calculation Phase**: FinancialCalculator computes totals, margins, monthly aggregations, and period comparisons
4. **Display Phase**: Components render metrics, charts, and analysis based on processed data
5. **Filter Phase**: Users can apply date range and category filters to refine analysis

### Session State Management
- `data_loaded`: Boolean flag indicating if financial data has been successfully loaded
- `financial_data`: Raw uploaded file data
- `processed_data`: Cleaned and validated DataFrame ready for analysis

## Recent Changes (July 22, 2025)

### Customer Analysis Integration
- **Added customer name requirement**: Added `Nama_Customer` as required column in data schema
- **Enhanced filtering**: Added customer-based filtering in sidebar alongside existing date and category filters
- **New analytics module**: Created `components/customer_metrics.py` for customer-specific analysis
- **Extended charts**: Added customer analysis charts in main charts component
- **Customer insights**: Includes top customer identification, revenue distribution, profitability analysis, and transaction trends
- **Multi-category support**: Added `components/customer_category_analysis.py` for analyzing customer behavior across multiple product categories
- **Cross-category analysis**: Customers can now purchase from multiple categories with detailed performance tracking

### Database Integration (Latest Update)
- **PostgreSQL Database**: Added complete database layer with SQLAlchemy ORM
- **Persistent Data Storage**: Financial transactions now stored in database instead of session state
- **Database Models**: Created `FinancialTransaction` and `DataUploadLog` models
- **Database Manager**: Implemented `DatabaseManager` class for all database operations
- **Data Source Selection**: Added option to choose between database and upload-only mode
- **Database Management Interface**: Added database statistics, upload history, and data export/clear functions
- **Auto-save on Upload**: Data automatically saved to database when uploaded

### Technical Updates
- Updated `DataProcessor` class to handle customer data validation and filtering
- Enhanced sidebar component with customer selection dropdown
- Added customer analysis to main dashboard flow
- Updated sample data templates to include customer information with multi-category examples
- Improved data upload instructions to emphasize customer name requirement and multi-category support
- Added customer-category matrix analysis with heatmaps and diversification metrics
- Implemented cross-category performance tracking for customers purchasing from multiple categories
- Integrated PostgreSQL database with complete CRUD operations and filtering capabilities

## External Dependencies

### Core Libraries
- **streamlit**: Web application framework and UI components
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive visualization library (express and graph_objects modules)
- **numpy**: Numerical computing support

### Additional Modules
- **datetime**: Date and time handling for temporal analysis
- **io.StringIO**: String buffer operations for file processing

## Deployment Strategy

### Local Development
- Standard Python environment with pip-installed dependencies
- Run with `streamlit run app.py`
- No database required - operates on uploaded file data

### Production Considerations
- Stateless application design suitable for cloud deployment
- File uploads processed in memory without persistent storage
- Session state management handles user data during session lifecycle
- Horizontal scaling possible due to stateless architecture

### Performance Optimization
- Data processing optimized for typical business financial datasets
- Monthly aggregation reduces computational complexity for large datasets
- Lazy loading of charts and metrics based on data availability
- Memory-efficient data processing with pandas operations

## Key Architectural Decisions

### Modular Component Design
**Problem**: Need maintainable and reusable UI components
**Solution**: Separate Python modules for each major UI section
**Rationale**: Improves code organization, enables independent component development, and facilitates testing

### Session State for Data Persistence
**Problem**: Maintain user data across Streamlit reruns without database
**Solution**: Streamlit session state for storing processed data
**Rationale**: Eliminates need for external storage while providing seamless user experience

### In-Memory Data Processing
**Problem**: Handle file uploads and processing without persistence layer
**Solution**: Process and store data entirely in memory during user session
**Rationale**: Simplifies deployment, reduces infrastructure requirements, suitable for analysis workflows

### Plotly for Visualizations
**Problem**: Need interactive, professional-quality charts
**Solution**: Plotly Express and Graph Objects for chart rendering
**Rationale**: Provides rich interactivity, professional appearance, and integrates well with Streamlit
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class FinancialCalculator:
    def __init__(self):
        pass
    
    def calculate_metrics(self, df):
        """Calculate key financial metrics from the dataframe"""
        if df.empty:
            return self._empty_metrics()
        
        # Basic totals
        total_revenue = df['Revenue'].sum()
        total_cogs = df['COGS'].sum()
        total_sales_commission = df['Sales_Commission'].sum()
        total_sales_program = df['Sales_Program'].sum()
        
        # Calculate gross profit and net profit
        gross_profit = total_revenue - total_cogs
        total_expenses = total_sales_commission + total_sales_program
        net_profit = gross_profit - total_expenses
        
        # Calculate margins
        gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
        net_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Monthly aggregation for trends
        df_monthly = self._calculate_monthly_metrics(df)
        
        # Period comparison
        current_period, previous_period = self._calculate_period_comparison(df)
        
        return {
            'totals': {
                'revenue': total_revenue,
                'cogs': total_cogs,
                'sales_commission': total_sales_commission,
                'sales_program': total_sales_program,
                'gross_profit': gross_profit,
                'net_profit': net_profit,
                'total_expenses': total_expenses
            },
            'margins': {
                'gross_margin': gross_margin,
                'net_margin': net_margin
            },
            'monthly_data': df_monthly,
            'period_comparison': {
                'current': current_period,
                'previous': previous_period
            }
        }
    
    def _empty_metrics(self):
        """Return empty metrics structure"""
        return {
            'totals': {
                'revenue': 0,
                'cogs': 0,
                'sales_commission': 0,
                'sales_program': 0,
                'gross_profit': 0,
                'net_profit': 0,
                'total_expenses': 0
            },
            'margins': {
                'gross_margin': 0,
                'net_margin': 0
            },
            'monthly_data': pd.DataFrame(),
            'period_comparison': {
                'current': None,
                'previous': None
            }
        }
    
    def _calculate_monthly_metrics(self, df):
        """Calculate monthly aggregated metrics"""
        if df.empty:
            return pd.DataFrame()
        
        df_copy = df.copy()
        df_copy['Year_Month'] = df_copy['Tanggal'].dt.to_period('M')
        
        monthly = df_copy.groupby('Year_Month').agg({
            'Revenue': 'sum',
            'COGS': 'sum',
            'Sales_Commission': 'sum',
            'Sales_Program': 'sum'
        }).reset_index()
        
        # Calculate derived metrics
        monthly['Gross_Profit'] = monthly['Revenue'] - monthly['COGS']
        monthly['Total_Expenses'] = monthly['Sales_Commission'] + monthly['Sales_Program']
        monthly['Net_Profit'] = monthly['Gross_Profit'] - monthly['Total_Expenses']
        monthly['Gross_Margin'] = (monthly['Gross_Profit'] / monthly['Revenue'] * 100).fillna(0)
        monthly['Net_Margin'] = (monthly['Net_Profit'] / monthly['Revenue'] * 100).fillna(0)
        
        # Convert period to string for plotting
        monthly['Month'] = monthly['Year_Month'].astype(str)
        
        return monthly
    
    def _calculate_period_comparison(self, df):
        """Calculate current vs previous period comparison"""
        if df.empty:
            return None, None
        
        # Determine period split
        max_date = df['Tanggal'].max()
        min_date = df['Tanggal'].min()
        total_days = (max_date - min_date).days
        
        if total_days <= 7:
            # Weekly comparison
            split_date = max_date - timedelta(days=total_days//2)
        elif total_days <= 60:
            # Monthly comparison
            split_date = max_date - timedelta(days=30)
        else:
            # Quarterly comparison
            split_date = max_date - timedelta(days=90)
        
        current_period = df[df['Tanggal'] > split_date]
        previous_period = df[df['Tanggal'] <= split_date]
        
        def calculate_period_metrics(period_df):
            if period_df.empty:
                return None
            
            return {
                'revenue': period_df['Revenue'].sum(),
                'cogs': period_df['COGS'].sum(),
                'sales_commission': period_df['Sales_Commission'].sum(),
                'sales_program': period_df['Sales_Program'].sum(),
                'gross_profit': period_df['Revenue'].sum() - period_df['COGS'].sum(),
                'net_profit': (period_df['Revenue'].sum() - period_df['COGS'].sum() - 
                              period_df['Sales_Commission'].sum() - period_df['Sales_Program'].sum())
            }
        
        return calculate_period_metrics(current_period), calculate_period_metrics(previous_period)
    
    def calculate_growth_rate(self, current, previous):
        """Calculate growth rate between periods"""
        if previous is None or previous == 0:
            return 0
        return ((current - previous) / previous) * 100
    
    def generate_summary_report(self, df, metrics):
        """Generate summary report for export"""
        summary_data = []
        
        # Add total metrics
        totals = metrics['totals']
        margins = metrics['margins']
        
        summary_data.append({
            'Metrik': 'Total Revenue',
            'Nilai': totals['revenue'],
            'Satuan': 'IDR'
        })
        
        summary_data.append({
            'Metrik': 'Total COGS',
            'Nilai': totals['cogs'],
            'Satuan': 'IDR'
        })
        
        summary_data.append({
            'Metrik': 'Total Komisi Penjualan',
            'Nilai': totals['sales_commission'],
            'Satuan': 'IDR'
        })
        
        summary_data.append({
            'Metrik': 'Total Program Penjualan',
            'Nilai': totals['sales_program'],
            'Satuan': 'IDR'
        })
        
        summary_data.append({
            'Metrik': 'Gross Profit',
            'Nilai': totals['gross_profit'],
            'Satuan': 'IDR'
        })
        
        summary_data.append({
            'Metrik': 'Net Profit',
            'Nilai': totals['net_profit'],
            'Satuan': 'IDR'
        })
        
        summary_data.append({
            'Metrik': 'Gross Margin',
            'Nilai': margins['gross_margin'],
            'Satuan': '%'
        })
        
        summary_data.append({
            'Metrik': 'Net Margin',
            'Nilai': margins['net_margin'],
            'Satuan': '%'
        })
        
        return pd.DataFrame(summary_data)

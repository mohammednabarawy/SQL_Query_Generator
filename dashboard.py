import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta
import re

def load_query_history():
    """Load query history from JSON file"""
    history_file = os.path.join("query_history", "history.json")
    
    if not os.path.exists(history_file):
        return []
    
    try:
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
        return history
    except Exception as e:
        st.error(f"Error loading query history: {e}")
        return []

def extract_tables_from_query(query):
    """Extract table names from SQL query using regex"""
    # This is a simple regex pattern - might need refinement for complex queries
    tables = re.findall(r'FROM\s+\[?(\w+)\]?|JOIN\s+\[?(\w+)\]?', query, re.IGNORECASE)
    # Flatten and clean the results
    return [table for sublist in tables for table in sublist if table]

def main():
    st.set_page_config(page_title="SQL Query History Dashboard", page_icon="📊", layout="wide")
    
    st.title("📊 SQL Query History Dashboard")
    st.markdown("Analyze your database query patterns and performance")
    
    # Load query history
    history = load_query_history()
    
    if not history:
        st.warning("No query history found. Start using the SQL Query Generator to build history.")
        return
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(history)
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Add date and hour columns for aggregation
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    
    # Extract tables from queries
    df['tables'] = df['sql_query'].apply(extract_tables_from_query)
    
    # Create dashboard
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Query Activity Over Time")
        
        # Group by date and count
        daily_counts = df.groupby('date').size().reset_index(name='count')
        
        # Plot
        fig = px.line(daily_counts, x='date', y='count', 
                     title='Queries Per Day',
                     labels={'count': 'Number of Queries', 'date': 'Date'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Query Success Rate")
        
        # Count success vs error
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        
        # Plot
        fig = px.pie(status_counts, values='Count', names='Status', 
                    title='Query Success Rate',
                    color_discrete_map={'success': 'green', 'error': 'red'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Most queried tables
    st.subheader("Most Queried Tables")
    
    # Explode the tables column to get one row per table
    table_df = df.explode('tables')
    
    # Count occurrences of each table
    table_counts = table_df['tables'].value_counts().reset_index()
    table_counts.columns = ['Table', 'Count']
    
    # Only show if we have tables
    if not table_counts.empty and not table_counts['Table'].isna().all():
        # Plot
        fig = px.bar(table_counts.head(10), x='Table', y='Count',
                    title='Top 10 Most Queried Tables',
                    labels={'Count': 'Number of Queries', 'Table': 'Table Name'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No table data available for analysis.")
    
    # Recent queries
    st.subheader("Recent Queries")
    
    # Show the 10 most recent queries
    recent = df.sort_values('timestamp', ascending=False).head(10)
    
    # Format for display
    for i, row in enumerate(recent.itertuples()):
        with st.expander(f"{i+1}. {row.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {row.user_request[:50]}{'...' if len(row.user_request) > 50 else ''}"):
            st.markdown("**User Request:**")
            st.write(row.user_request)
            
            st.markdown("**Generated SQL:**")
            st.code(row.sql_query, language="sql")
            
            st.markdown(f"**Status:** {'✅ Success' if row.status == 'success' else '❌ Error'}")
            
            if hasattr(row, 'error') and row.error:
                st.error(row.error)

if __name__ == "__main__":
    main()

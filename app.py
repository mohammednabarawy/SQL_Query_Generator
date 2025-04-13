import streamlit as st
import pandas as pd
from ollama_mssql import connect_db, get_db_schema_and_samples, ask_ollama_for_sql

def main():
    st.set_page_config(page_title="SQL Query Generator", page_icon="🔍", layout="wide")
    
    st.title("🔍 SQL Query Generator")
    st.markdown("Ask questions about your database in plain English")
    
    # Initialize connection
    if 'conn' not in st.session_state:
        try:
            with st.spinner("Connecting to database..."):
                st.session_state.conn = connect_db()
                st.session_state.schema = get_db_schema_and_samples(st.session_state.conn)
                st.success("Connected to database successfully!")
        except Exception as e:
            st.error(f"Failed to connect to database: {e}")
            return
    
    # User input
    user_input = st.text_area("💬 Ask your question about the database:", 
                             placeholder="e.g., Show all employees hired this year")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        model = st.selectbox("Select model:", ["llama3", "codellama", "mistral"])
        
    with col2:
        if st.button("Generate SQL Query", type="primary", use_container_width=True):
            if not user_input:
                st.warning("Please enter a question")
                return
                
            with st.spinner("Generating SQL query..."):
                # Get SQL query
                sql_query = ask_ollama_for_sql(user_input, st.session_state.schema, model)
                
                # Display the query
                st.code(sql_query, language="sql")
                
                # Execute query
                try:
                    cursor = st.session_state.conn.cursor()
                    cursor.execute(sql_query)
                    
                    if cursor.description:  # SELECT query
                        columns = [col[0] for col in cursor.description]
                        rows = cursor.fetchall()
                        
                        # Convert to pandas DataFrame for better display
                        df = pd.DataFrame.from_records(rows, columns=columns)
                        st.dataframe(df, use_container_width=True)
                        
                        # Add download button
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Download results as CSV",
                            csv,
                            "query_results.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    else:
                        st.session_state.conn.commit()
                        st.success("Query executed successfully (non-SELECT query)")
                except Exception as e:
                    st.error(f"Error executing SQL: {e}")
    
    # Show schema in expander
    with st.expander("View Database Schema"):
        st.text(st.session_state.schema)

if __name__ == "__main__":
    main()

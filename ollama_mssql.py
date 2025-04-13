import os
import pyodbc
import requests
import json
from datetime import datetime


def connect_db():
    db_username = "sa"
    db_password = "123"
    db_server = "NUCBOX\\SQLEXPRESS"
    db_database = "Aghna_contracting_2025"

    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={db_server};"
        f"DATABASE={db_database};"
        f"UID={db_username};"
        f"PWD={db_password};"
    )

    return pyodbc.connect(conn_str)


def ensure_db_context_folder():
    folder = os.path.join(os.path.dirname(__file__), "db_context")
    os.makedirs(folder, exist_ok=True)
    return folder


def get_db_schema_and_samples(conn, sample_limit=10):
    cursor = conn.cursor()
    schema_str = ""
    context_folder = ensure_db_context_folder()

    # Get tables
    cursor.execute("""
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
    """)
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
        schema_str += f"\n🧾 Table: {table}\nColumns:\n"

        # Columns with more details
        cursor.execute("""
            SELECT 
                c.COLUMN_NAME, 
                c.DATA_TYPE, 
                c.CHARACTER_MAXIMUM_LENGTH,
                c.IS_NULLABLE,
                COLUMNPROPERTY(OBJECT_ID(c.TABLE_SCHEMA + '.' + c.TABLE_NAME), c.COLUMN_NAME, 'IsIdentity') as IS_IDENTITY,
                CASE WHEN pk.COLUMN_NAME IS NOT NULL THEN 'PK' ELSE '' END as IS_PRIMARY_KEY
            FROM INFORMATION_SCHEMA.COLUMNS c
            LEFT JOIN (
                SELECT ku.TABLE_CATALOG, ku.TABLE_SCHEMA, ku.TABLE_NAME, ku.COLUMN_NAME
                FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
                JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS ku
                    ON tc.CONSTRAINT_TYPE = 'PRIMARY KEY' 
                    AND tc.CONSTRAINT_NAME = ku.CONSTRAINT_NAME
            ) pk 
            ON c.TABLE_CATALOG = pk.TABLE_CATALOG
                AND c.TABLE_SCHEMA = pk.TABLE_SCHEMA
                AND c.TABLE_NAME = pk.TABLE_NAME
                AND c.COLUMN_NAME = pk.COLUMN_NAME
            WHERE c.TABLE_NAME = ?
            ORDER BY c.ORDINAL_POSITION
        """, table)
        
        columns = cursor.fetchall()
        col_names = [col[0] for col in columns]

        for col_name, col_type, max_length, is_nullable, is_identity, is_pk in columns:
            type_info = f"{col_type}"
            if max_length and max_length > 0:
                type_info += f"({max_length})"
            
            constraints = []
            if is_pk:
                constraints.append("PK")
            if is_identity:
                constraints.append("Identity")
            if is_nullable == "NO":
                constraints.append("NOT NULL")
                
            constraints_str = " ".join(constraints)
            if constraints_str:
                constraints_str = f" [{constraints_str}]"
                
            schema_str += f" - {col_name} ({type_info}){constraints_str}\n"

        # Sample data for table file
        sample_rows = []
        try:
            cursor.execute(f"SELECT TOP {sample_limit} * FROM [{table}]")
            rows = cursor.fetchall()

            if rows:
                sample_rows.append("\t".join(col_names))
                for row in rows:
                    sample_rows.append(
                        "\t".join(str(val) if val is not None else "NULL" for val in row))
        except Exception as e:
            sample_rows.append(f"(Could not retrieve sample rows: {e})")

        # Save table sample to separate file
        table_file = os.path.join(context_folder, f"{table}.txt")
        with open(table_file, "w", encoding="utf-8") as tf:
            tf.write(f"Sample rows from table: {table}\n\n")
            tf.write("\n".join(sample_rows))

    # Add foreign key relationships
    schema_str += "\n🔗 Foreign Key Relationships:\n"
    cursor.execute("""
        SELECT 
            fk.name AS FK_Name,
            tp.name AS ParentTable,
            cp.name AS ParentColumn,
            tr.name AS RefTable,
            cr.name AS RefColumn
        FROM sys.foreign_keys fk
        INNER JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        INNER JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
        INNER JOIN sys.columns cp ON fkc.parent_column_id = cp.column_id AND cp.object_id = tp.object_id
        INNER JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
        INNER JOIN sys.columns cr ON fkc.referenced_column_id = cr.column_id AND cr.object_id = tr.object_id
    """)
    for fk_name, parent, parent_col, ref, ref_col in cursor.fetchall():
        schema_str += f" - {parent}({parent_col}) ➝ {ref}({ref_col})\n"

    # Add indexes information
    schema_str += "\n📊 Indexes:\n"
    cursor.execute("""
        SELECT 
            t.name AS TableName,
            ind.name AS IndexName,
            col.name AS ColumnName,
            ind.is_unique AS IsUnique,
            ind.is_primary_key AS IsPrimaryKey
        FROM 
            sys.indexes ind 
        INNER JOIN 
            sys.index_columns ic ON ind.object_id = ic.object_id AND ind.index_id = ic.index_id 
        INNER JOIN 
            sys.columns col ON ic.object_id = col.object_id AND ic.column_id = col.column_id 
        INNER JOIN 
            sys.tables t ON ind.object_id = t.object_id 
        WHERE 
            ind.is_primary_key = 0 
            AND ind.is_unique_constraint = 0 
            AND t.is_ms_shipped = 0 
        ORDER BY 
            t.name, ind.name, ic.key_ordinal
    """)
    
    current_index = ""
    for table_name, index_name, column_name, is_unique, is_pk in cursor.fetchall():
        if index_name != current_index:
            current_index = index_name
            unique_str = "UNIQUE " if is_unique else ""
            pk_str = "PRIMARY KEY " if is_pk else ""
            schema_str += f" - {table_name}: {unique_str}{pk_str}Index {index_name} on "
        schema_str += f"{column_name}, "
    
    # Remove trailing comma from last index
    if schema_str.endswith(", "):
        schema_str = schema_str[:-2] + "\n"

    # Save schema to file
    schema_file_path = os.path.join(context_folder, "schema.txt")
    with open(schema_file_path, "w", encoding="utf-8") as f:
        f.write(schema_str)

    return schema_str


def ask_ollama_for_sql(user_request, schema, model="llama3"):
    prompt = f"""
You are an expert MSSQL query generator.

Here is the database schema:
{schema}

Based on the above schema and table samples, generate the SQL query for this request:

\"\"\"{user_request}\"\"\"

Only return the SQL query. No explanation or formatting.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json().get("response", "").strip()
    except Exception as e:
        return f"❌ Error contacting Ollama: {e}"


def execute_sql_query(conn, sql_query):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_query)

        if cursor.description:  # SELECT
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            print("\n✅ Query Result:\n")
            print("\t".join(columns))
            for row in rows:
                print("\t".join(str(x) for x in row))
            
            # Return results for potential further processing
            return {"columns": columns, "rows": rows}
        else:
            conn.commit()
            print("\n✅ Query executed successfully.")
            return {"message": "Query executed successfully (non-SELECT query)"}
    except Exception as e:
        error_msg = f"\n❌ Error executing SQL: {e}"
        print(error_msg)
        return {"error": error_msg}


def save_query_history(user_request, sql_query, result=None, error=None):
    """Save query history to a JSON file"""
    history_folder = os.path.join(os.path.dirname(__file__), "query_history")
    os.makedirs(history_folder, exist_ok=True)
    
    history_file = os.path.join(history_folder, "history.json")
    
    # Load existing history
    if os.path.exists(history_file):
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []
    
    # Add new entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_request": user_request,
        "sql_query": sql_query,
        "status": "error" if error else "success"
    }
    
    if error:
        entry["error"] = str(error)
    
    history.append(entry)
    
    # Save updated history
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def get_available_models():
    """Get list of available models from Ollama"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = [model["name"] for model in response.json().get("models", [])]
        return models
    except:
        # Return default models if Ollama is not available
        return ["llama3", "codellama", "mistral"]


def main():
    conn = connect_db()
    schema = get_db_schema_and_samples(conn)

    print("💬 Ask your question about the database (e.g., 'Show all employees hired this year'):")
    user_input = input("👉 ")

    # Get available models
    models = get_available_models()
    if models:
        print(f"\nAvailable models: {', '.join(models)}")
        model = input(f"Select model (default: llama3): ") or "llama3"
    else:
        model = "llama3"

    sql_query = ask_ollama_for_sql(user_input, schema, model)
    print(f"\n🧠 Generated SQL:\n{sql_query}")

    result = execute_sql_query(conn, sql_query)
    
    # Save query to history
    save_query_history(user_input, sql_query, 
                      result=None if "error" in result else result,
                      error=result.get("error"))


if __name__ == "__main__":
    main()

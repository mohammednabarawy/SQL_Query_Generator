import os
import pyodbc
import requests


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

        # Columns
        cursor.execute("""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = ?
        """, table)
        columns = cursor.fetchall()
        col_names = [col[0] for col in columns]

        for col_name, col_type in columns:
            schema_str += f" - {col_name} ({col_type})\n"

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

    # Save schema to file
    schema_file_path = os.path.join(context_folder, "schema.txt")
    with open(schema_file_path, "w", encoding="utf-8") as f:
        f.write(schema_str)

    return schema_str


def ask_ollama_for_sql(user_request, schema):
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
                "model": "llama3",
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
        else:
            conn.commit()
            print("\n✅ Query executed successfully.")
    except Exception as e:
        print(f"\n❌ Error executing SQL: {e}")


def main():
    conn = connect_db()
    schema = get_db_schema_and_samples(conn)

    print("💬 Ask your question about the database (e.g., 'Show all employees hired this year'):")
    user_input = input("👉 ")

    sql_query = ask_ollama_for_sql(user_input, schema)
    print(f"\n🧠 Generated SQL:\n{sql_query}")

    execute_sql_query(conn, sql_query)


if __name__ == "__main__":
    main()

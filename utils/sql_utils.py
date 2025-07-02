# utils/sql_utils.py
import pyodbc
import os

def extract_documents_from_sql():
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('SQL_SERVER')};"
        f"DATABASE={os.getenv('SQL_DATABASE')};"
        f"UID={os.getenv('SQL_USER')};"
        f"PWD={os.getenv('SQL_PASSWORD')}"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, titre, contenu FROM procedures")
    rows = cursor.fetchall()
    return [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]

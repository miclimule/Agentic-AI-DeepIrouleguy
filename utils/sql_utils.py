# utils/sql_utils.py
import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()
# def extract_documents_from_sql():
#     conn = pyodbc.connect(
#         f"DRIVER={{ODBC Driver 17 for SQL Server}};"
#         f"SERVER={os.getenv('SQL_SERVER')};"
#         f"DATABASE={os.getenv('SQL_SERVER_DATABASE')};"
#         f"UID={os.getenv('SQL_SERVER_USERNAME')};"
#         f"PWD={os.getenv('SQL_SERVER_PASSWORD')}"
#     )
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, titre, contenu FROM procedures")
#     rows = cursor.fetchall()
#     return [{"id": row[0], "title": row[1], "content": row[2]} for row in rows]

# Configuration de la connexion

server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_SERVER_DATABASE')
username = os.getenv('SQL_SERVER_USERNAME')
password = os.getenv('SQL_SERVER_PASSWORD')  

# print(pyodbc.drivers())
# print("server : ",server)
# print("database : ",database)
# print("user : ",username)
# print("pwd : ",password)

# Chaîne de connexion ODBC
connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

# Connexion et test
try:
    conn = pyodbc.connect(connection_string)
    print("Connexion réussie à SQL Server !")

    # Exemple de requête : lister les tables
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
    tables = cursor.fetchall()
    for row in tables:
        print("Table trouvée :", row.TABLE_NAME)

    conn.close()
except Exception as e:
    print("❌ Erreur de connexion :", e)


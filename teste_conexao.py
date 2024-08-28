import mysql.connector
import os

db_config = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', '1234'),
    'host': os.getenv('DB_HOST', 'mysql_db'),  
    'database': os.getenv('DB_NAME', 'my_database')
}

try:
    conn = mysql.connector.connect(**db_config)
    if conn.is_connected():
        print("Conexão com o banco de dados estabelecida com sucesso.")
    conn.close()
except mysql.connector.Error as err:
    print(f"Erro ao conectar ao banco de dados: {err}")

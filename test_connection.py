import psycopg2

try:
    conn = psycopg2.connect(
        dbname="whatsapp_bot",
        user="postgres",
        password="Ctbapr32",
        host="localhost",
        port="5432"
    )
    print("Conexão bem-sucedida!")
    conn.close()

except Exception as e:
    print(f"Erro ao conectar: {e}")


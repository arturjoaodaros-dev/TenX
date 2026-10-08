from App.Database.connector import conn
with conn.cursor() as cursor:
    cursor.execute("SELECT current_database(), current_schema()")
    print("BANCO/SCHEMA:", cursor.fetchone())

    cursor.execute("SELECT current_user")
    print("USUÁRIO:", cursor.fetchone())

    cursor.execute("""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_name = 'usuarios'
    """)
    print("TABELAS:", cursor.fetchall())

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    print("TOTAL USUARIOS:", cursor.fetchone())

    cursor.execute("SELECT * FROM usuarios LIMIT 10")
    print("USUARIOS:", cursor.fetchall())

with conn.cursor() as cursor:
    cursor.execute("SELECT usuario_id FROM usuarios LIMIT 20")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM usuarios WHERE usuario_id = 1")
    print(cursor.fetchall())
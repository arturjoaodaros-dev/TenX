import os
import psycopg
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
def Query(query, params=None) -> list:
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            if cursor.description:
                dados = cursor.fetchall()
                colunas = [desc.name for desc in cursor.description]

                conn.commit()

                return [
                    dados, 
                    colunas, 
                    pd.DataFrame(dados, columns=colunas)]

            resultado = cursor.statusmessage

            return [resultado]
    except Exception as e:
        print("Algo de de errado, nada foi alterado. ERR:", e)
        conn.rollback()
        return ["Algo de de errado, nada foi alterado. ERR:", e]
        

    finally:
        conn.commit()
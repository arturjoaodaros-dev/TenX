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
    password=os.getenv("DB_PASSWORD"),
    autocommit=False
)

def Query(
    query: str,
    params=None,
    return_info: str = "",
    autocommit: bool = True
) -> list:
    modo = (return_info or "").strip().lower()

    if modo not in ("", "data", "columns", "table"):
        raise ValueError(
            "return_info deve ser '', 'data', 'columns' ou 'table'."
        )

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)# type: ignore[arg-type]

            if cursor.description:
                dados = cursor.fetchall()
                colunas = [
                    desc.name for desc in cursor.description
                ]

                if modo == "data":
                    resultado = dados

                elif modo == "columns":
                    resultado = colunas

                elif modo == "table":
                    resultado = [
                        pd.DataFrame(dados, columns=colunas)
                    ]

                else:
                    resultado = [
                        dados,
                        colunas,
                        pd.DataFrame(dados, columns=colunas)
                    ]

            else:
                resultado = [cursor.statusmessage]

        # Confirma a transação uma única vez.
        if autocommit:
            conn.commit()

        return resultado

    except Exception:
        conn.rollback()
        raise
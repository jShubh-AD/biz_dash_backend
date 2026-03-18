import io
import pandas as pd
from sqlalchemy import text

def copy_to_postgres(df: pd.DataFrame, table_name: str, engine):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    with engine.raw_connection() as conn:
        cursor = conn.cursor()

        # create table dynamically
        cols = ", ".join([f"{col} TEXT" for col in df.columns])
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({cols});")

        # copy
        cursor.copy_expert(
            f"COPY {table_name} FROM STDIN WITH CSV",
            buffer
        )

        conn.commit()
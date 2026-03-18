import io

def copy_to_postgres(df, table_name: str, engine):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)

    with engine.raw_connection() as conn:
        cursor = conn.cursor()

        # create table safely (all TEXT)
        cols = ", ".join([f'"{col}" TEXT' for col in df.columns])
        cursor.execute(f'CREATE TABLE IF NOT EXISTS "{table_name}" ({cols});')

        try:
            cursor.copy_expert(
                f'COPY "{table_name}" FROM STDIN WITH (FORMAT CSV)',
                buffer
            )
        except Exception as e:
            conn.rollback()
            raise e

        conn.commit()
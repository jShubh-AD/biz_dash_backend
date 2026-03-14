# services/db_service.py
from sqlalchemy import text
from app.db.session import SessionLocal

async def run_query(sql: str):
    db = SessionLocal()
    try:
        result = db.execute(text(sql))
        rows = result.fetchall()
        cols = result.keys()
        return rows, cols
        # return [dict(zip(cols, r)) for r in rows]
    finally:
        db.close()
# services/db_service.py
from sqlalchemy import text
import logging
from app.utils.logger import get_logger
from app.db.session import SessionLocal

async def run_query(sql: str):
    logger = get_logger('run_query')
    db = SessionLocal()
    try:
        result = db.execute(text(sql))
        rows = result.fetchall()
        cols = result.keys()
        logger.info(f"[SQL:{sql}] Results: {rows, cols}")
        return rows, cols
        # return [dict(zip(cols, r)) for r in rows]
    finally:
        db.close()
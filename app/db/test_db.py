from app.db.session import SessionLocal
from sqlalchemy import text

db = SessionLocal()
result = db.execute(text("SELECT COUNT(*) FROM videos"))
print(result.fetchone())
db.close()
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.db.session import engine
from app.api.http.dependencies.room_id import validate_room
from app.api.ws.manager import manager
from app.utils.csv_cleaner import clean_columns
from app.models.chat import ChatRoom, Schema
import os
from dotenv import load_dotenv
import pandas as pd
from app.utils.csv_loader import copy_to_postgres
from app.utils.logger import get_logger
from app.db.session import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

load_dotenv()

router = APIRouter()

Max_Size = int(os.getenv('MAX_CSV_SIZE'))
Chunk_Size = int(os.getenv('CHUNK_SIZE'))
Max_Row = int(os.getenv('MAX_ROWS'))

@router.post('/csv/{room_id}')
async def uplaod_csv(
    room : ChatRoom = Depends(validate_room),
    file: UploadFile = File(...),
    ):

    try:
         # validate file
        if not file.filename.endswith('.csv'):
            raise HTTPException(400, "Only CSV allowed")
        
        contents = await file.read()

        if len(contents) > Max_Size:
            raise HTTPException(400, "File too large")
        
        try:
            df = pd.read_csv(pd.io.common.BytesIO(contents))
        except Exception as e:
            print(e)
            raise HTTPException(400, "Invalid CSV")

        if len(df) > Max_Row:
            raise HTTPException(400, "Too many rows")
        
        # clean columns
        df.columns = clean_columns(df.columns)
        df = df.drop_duplicates()

        table_name = f"room_{str(room.room_id).replace('-', '_')}"
        copy_to_postgres(df,table_name,engine)

        room.table_name = table_name
        room.schema.columns = list(df.columns)
        room.schema.sample = df.head(5).to_dict()
        room.have_db= True

        return {
            "success": True,
            "table_name": table_name,
            "columns": room.schema.columns,
            'have_db':True,
            "rows": len(df)
        }
    except HTTPException as e:
        print(e)
        raise e

    except Exception as e:
        print("CSV Upload Error:", e)
        raise HTTPException(500, "Something went wrong")
    

@router.delete('/csv/{room_id}')
async def delete_csv(room: ChatRoom = Depends(validate_room), db : Session = Depends(get_db)):
    logger = get_logger('delete_csv')
    try:
        table_name = room.table_name
        if not table_name or room.have_db == False:
            raise HTTPException(400, detail='No table name with in the room')
        
        db.execute(text(f'DROP TABLE IF EXISTS "{table_name}"'))
        db.commit()

        room.have_db = False
        room.table_name = None
        room.schema = Schema()

        return{
            "success": True,
            "status":200,
            "table_name": table_name,
            "message": 'Table deleted successfully',
        }
    
    except HTTPException as e:
        raise e

    except Exception as e:
        db.rollback()
        logger.exception(f'[API EXCP]: {e}')
        raise HTTPException(500, detail="Failed to delete table")
        
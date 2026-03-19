from app.services.gemini_client import ask_llm
from app.models.chat import ChatRoom
import json
import logging
from app.utils.logger import get_logger
import re

class ChartSelectorAgent:
    async def select(self, query: str, cols: list, rows: list, room: ChatRoom):
        sample = rows[:5]

        logger = get_logger("chart_selector")

        prompt = f"""
            You are a BI visualization expert.

            User query:
            {query}

            Columns:
            {cols}

            Sample data:
            {sample}

            Choose best chart.

            Rules:
            - 1 col:
                numeric → kpi or histogram
            - 2 cols:
                both numeric → scatter
                else:
                    if time → line
                    elif <=5 categories → pie
                    else → bar
            - 3 cols:
                if time → multi-line
                else → grouped bar
            - >3 → table

            ANY OTHER OUTPUT EXCEPT GIVEN BELOW IS COMPLETELY REJECTED AND MIGTH BE TREATED AS ERROR
            ONLY Return JSON:
            {{
            "chart_type": "...",
            "reason": "short"
            }}
        """

        response = await ask_llm(prompt, room)
        logger.info(f"[room:{room.room_id}] RAW: {response}")
        try:
            cleaned = re.sub(r"```json\s*", "", response)
            cleaned = re.sub(r"```", "", cleaned).strip()
            data = json.loads(cleaned.strip())
            logger.info(f"[room:{room.room_id}] PARSED: {data}")
            return data
        except:
            logger.exception(f"[room:{room.room_id}] JSON PARSE FAILED")
            return {"chart_type": "table", "reason": "fallback"}
from app.services.gemini_client import ask_llm
from app.services.db_service import run_query
from app.services.schema_service import SCHEMA
from app.models.chat import ChatRoom
import logging
import time
from app.utils.logger import get_logger
import re

class SQLAgent:
    logger = get_logger("sql_agent")

    async def generate_sql(self, query: str, is_chart: bool, room: ChatRoom):
        system_prompt = f"""
            You are a senior BI engineer generating PostgreSQL queries.

           Rules:
           - ONLY SELECT
           - Use ONLY given schema
           - ALWAYS LIMIT 50 unless speified otherwise
           - Prefer simple queries over complex joins
           - Use aggregation when needed (SUM, COUNT, AVG)
           - Use GROUP BY when aggregating
           - Use ORDER BY for time/date columns
           - Handle NULLs using COALESCE
           - Alias columns clearly

            DATA TYPE HANDLING (CRITICAL):
            - All columns are stored as TEXT
            - You MUST infer correct types
            Rules:
            - Numeric → CAST(NULLIF(column, '') AS FLOAT)
            - Integer → CAST(NULLIF(column, '') AS INTEGER)
           CRITICAL DATE RULE (STRICT):
                - NEVER use CAST(column AS DATE) or CAST(column AS TIMESTAMP)
                - This will cause errors and is INVALID

                - If column is in DATE FORMATS:
                    - MUST use:
                        TO_TIMESTAMP(column, format)

                - Example (CORRECT):
                    DATE(TO_TIMESTAMP(issue_reported_at, 'DD/MM/YYYY HH24:MI'))

                - Any use of CAST for date = WRONG OUTPUT


            - ALWAYS cast before:
                - SUM / AVG
                - comparisons
                - ORDER BY

            - NEVER perform operations on raw TEXT

            CRITICAL:
            - ALWAYS use EXACT table name: {room.table_name}
            - DO NOT guess or modify table name

            SCHEMA:
            - ALWAYS use EXACT columns name: {room.schema.columns}
            - DO NOT guess or modify column name

            DATE FORMATS:
                {room.schema.date_formats}

            SAMPLE DATA:
            {room.schema.sample}
            """

        chart_rule = """
            CHART DATA SHAPE RULES (CRITICAL):
            Detect intent and return correct structure:

            1. SINGLE VALUE:
            - 1 column (numeric, aggregated)

            2. CATEGORY/TIME COMPARISON:
            - 2 columns:
                - label (category/date)
                - value (aggregated numeric)
            - MUST GROUP BY label

            3. MULTI-SERIES:
            - 3 columns:
                - x-axis (time/category)
                - series (category)
                - value (aggregated)
            - MUST GROUP BY all non-aggregated columns

            4. RELATIONSHIP:
            - 2 numeric columns
            - NO aggregation
            - NO GROUP BY

            5. DISTRIBUTION:
            - 1 numeric column
            - NO aggregation

            - Use ORDER BY for time
            """ if is_chart else """
            Return rows that directly answer the question.
        """

        user_prompt = f"""
            User query:
            {query}

            {chart_rule}
            """

        output = """
            Return ONLY raw SQL. No markdown. No explanation.
            """

        prompt = system_prompt + user_prompt + output
        response = (await ask_llm(prompt, room)).strip() 
        clean_sql = self.clean_sql(response)
        self.logger.info(f"[room:{room.room_id}] FINAL_SQL: {clean_sql}")
        return clean_sql

    def clean_sql(self,sql: str):
        sql = re.sub(r"```sql\s*", "", sql)
        sql = re.sub(r"```", "", sql)
        return sql.strip()


    async def execute(self, sql: str):
        return await run_query(sql)
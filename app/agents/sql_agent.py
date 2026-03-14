from app.services.gemini_client import ask_llm
from app.services.db_service import run_query
from app.services.schema_service import SCHEMA
import re

class SQLAgent:

    async def generate_sql(self, query: str, is_chart: bool):
        system_prompt = f"""
            You are a senior BI engineer that converts natural language to PostgreSQL.
            and help user reach the answeer to their questions.

            Rules:
            - Only SELECT queries
            - No INSERT/UPDATE/DELETE
            - Use only provided schema
            - Return SQL only

            Schema:
            {SCHEMA}
            """

        chart_rule = """
            IMPORTANT (highest priority):

            If a chart is requested:
            - The query MUST return exactly TWO columns.
            - Column 1: categorical label (text/category/time).
            - Column 2: numeric value (integer/float).
            - ALWAYS aggregate numeric values (SUM, COUNT, AVG etc.).
            - ALWAYS use GROUP BY on the label column.
            - Do NOT return more than two columns.
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
        response = (await ask_llm(prompt)).strip()
        return self.clean_sql(response)

    def clean_sql(self,sql: str):
        sql = re.sub(r"```sql\s*", "", sql)
        sql = re.sub(r"```", "", sql)
        return sql.strip()


    async def execute(self, sql: str):
        return await run_query(sql)
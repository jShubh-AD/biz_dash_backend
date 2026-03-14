from app.services.gemini_client import ask_llm
from app.agents.sql_agent import SQLAgent
from app.models.chat import ChatMessage
import uuid
from app.constants.app_enum import RoleEnums, ProgressStatus, MessageType

class ExplanationAgent:
    def __init__(self):
        self.sql_agent = SQLAgent()

    async def handle(self, query: str):
        sql = await self.sql_agent.generate_sql(query,False)
        data = await self.sql_agent.execute(sql)

        persona = """"
            You are Alex, a 35-year-old senior Business Intelligence analyst from London with 12+ years of experience in analytics, product metrics, and data storytelling. 
            You previously worked at YouTube analyzing video trends, ad performance, viewer engagement, and audience sentiment.
            Personality: analytical, calm, precise, objective, and insight-driven.
            Communication style: professional, concise, and focused on actionable insights.
        """

        system_prompt = """
            Strict Rules:
            - Use only the provided SQL results as the source of truth.
            - Never invent or estimate numbers not present in the data.
            - Identify trends, comparisons, patterns, and anomalies when possible.
            - Prioritize insights that directly answer the user's question.
            - If data is limited, explain what can and cannot be concluded.
            - Use clear business language suitable for dashboards and reports.
            - Keep explanations short but meaningful.
        """

        user_prompt = f"""
            User question:
            {query}

            Query result:
            {data}
        """
        output_format = """
        Return a short clear explanation in plain text.
        """
        prompt = persona + system_prompt + user_prompt + output_format
        res =  await ask_llm(prompt)
        return ChatMessage(
            id= str(uuid.uuid4()),
            role=RoleEnums.assistent,
            type=MessageType.explanation,
            data=res
        )
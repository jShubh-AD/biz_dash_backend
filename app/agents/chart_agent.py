from app.agents.sql_agent import SQLAgent

class ChartAgent:

    def __init__(self):
        self.sql_agent = SQLAgent()

    async def handle(self, query: str):
        sql = await self.sql_agent.generate_sql(query, True)
        rows, cols = await self.sql_agent.execute(sql)
        labels = [r[0] for r in rows]
        values = [r[1] for r in rows]
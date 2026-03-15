from app.agents.sql_agent import SQLAgent
from app.models.chat import ChartData, ChatMessage, ChatRoom
from app.constants.app_enum import MessageType, RoleEnums
import uuid

class ChartAgent:

    def __init__(self):
        self.sql_agent = SQLAgent()

    async def handle(self, query: str, room: ChatRoom):
        sql = await self.sql_agent.generate_sql(query, True, room=room)
        rows, cols = await self.sql_agent.execute(sql)
        labels, values = zip(*rows) if rows else ([], [])
        cols = list(cols)
        return ChatMessage(
            id=str(uuid.uuid4()),
            data=ChartData(
                    labels=list(labels), 
                    values=list(values),
                    x_axis = cols[0],
                    y_axis = cols[1]
                ).model_dump(),
            type=MessageType.chart,
            role=RoleEnums.assistent
        )
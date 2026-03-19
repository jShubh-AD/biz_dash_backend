from app.agents.sql_agent import SQLAgent
from app.models.chat import ChartData, ChatMessage, ChatRoom, Dataset
from app.agents.chart_selector import ChartSelectorAgent
from app.constants.app_enum import MessageType, RoleEnums
import uuid

class ChartAgent:

    def __init__(self):
        self.sql_agent = SQLAgent()
        self.selector = ChartSelectorAgent()

    async def handle(self, query: str, room: ChatRoom):
        sql = await self.sql_agent.generate_sql(query, True, room=room)
        rows, cols = await self.sql_agent.execute(sql)
        # labels, values = zip(*rows) if rows else ([], [])
        cols = list(cols)

        chart_meta = await self.selector.select(query, cols, rows, room)
        chart_type = chart_meta.get("chart_type") 
        chart_reasson = chart_meta.get("reason")
        datasets = []

        if len(cols) == 1:
            datasets = [Dataset(label=cols[0], data=[float(r[0] or 0) for r in rows])]
            labels = list(range(len(rows)))

        elif len(cols) == 2:
            labels = [r[0] for r in rows]
            datasets = [Dataset(label=cols[1], data=[float(r[1] or 0) for r in rows])]

        elif len(cols) == 3:
            grouped = {}
            for x, cat, val in rows:
                grouped.setdefault(cat, []).append((x, float(val or 0)))

            labels = sorted(list(set(r[0] for r in rows)))

            for cat, vals in grouped.items():
                val_map = dict(vals)
                datasets.append(
                    Dataset(
                        label=str(cat),
                        data=[val_map.get(l, 0) for l in labels]
                    )
                )

        else:
            labels, datasets = [], []

        return ChatMessage(
            id=str(uuid.uuid4()),
            data=ChartData(
                chart_type=chart_type,
                reason= chart_reasson,
                labels=list(labels), 
                datasets=datasets,
                x_axis=cols[0] if cols else "",
                y_axis=cols[1] if len(cols) > 1 else ""
                ).model_dump(),
            type=MessageType.chart,
            sql_query=sql,
            role=RoleEnums.assistent
        )
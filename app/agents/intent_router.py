from app.services.gemini_client import ask_llm

async def route_intent(query: str):
    prompt = f"""
Classify user query into one intent:
generate_chart
explain

Query: {query}

Return only the intent and simply the query.
"""
    return await ask_llm(prompt)
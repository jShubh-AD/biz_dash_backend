from app.models.chat import ChatRoom

async def ask_llm(prompt: str, room: ChatRoom) -> str:
    if not room.api_key:
        raise Exception("API key not configured for this room")
    
    if not room.client:
        raise Exception("AI model not configured for this room")

    response = room.client.models.generate_content(
        model=f"models/{room.ai_model}",
        contents=prompt,
        config={
            "temperature": 0,
            "top_p": 0.8,
            "top_k": 20,
            "max_output_tokens": 200,
        }
    )

    return response.text.strip()
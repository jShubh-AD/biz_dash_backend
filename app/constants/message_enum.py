from enum import Enum

class MessageType (str,Enum):
    query= "query"
    explanation = "explanation"
    bar = "bar"
    pie = "pie"
    error = "error"
from typing import Annotated, Literal, Optional
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from pydantic import BaseModel, Field
from langchain_core.messages import MessageLikeRepresentation
from typing import Union
from langchain_core.messages import convert_to_messages, message_chunk_to_message
from langchain_core.messages import BaseMessageChunk
from typing import cast

class Graph_State(TypedDict):
    #messages: Annotated[list[AnyMessage], add_messages]
    generation_prompt: str
    reflection_prompt: str
    user_prompt: str
    user_advice: str
    content: str
    reflecton_advice: str
    reflect_count: int
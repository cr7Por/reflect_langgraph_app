from langgraph.graph import MessageGraph
from langchain_core.messages import BaseMessage
from typing import List
from langgraph.graph import END
from state import Graph_State

def generate_node(state: Graph_State):
    return [AIMessage(content="生成内容")]

def reflection_node(state: Graph_State):
    return [AIMessage(content="反思内容")]

builder = MessageGraph()
builder.add_node("generate", generate_node)
builder.add_node("reflect", reflection_node)
builder.set_entry_point("generate")


def should_continue(state: Graph_State):
    if state["reflect_count"] > 3:
        return END
    return "reflect"


builder.add_conditional_edges("generate", should_continue)
builder.add_edge("reflect", "generate")
graph = builder.compile()
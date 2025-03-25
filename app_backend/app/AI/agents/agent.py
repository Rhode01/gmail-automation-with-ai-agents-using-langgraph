from langgraph.graph import StateGraph, END
from langgraph.checkpoint import memory
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, AIMessage
from typing import Annotated, TypedDict,List
from operator import add
from pydantic import Field
import os

class agentState(StateGraph):
    content: str
    has_attachment:bool = Field(..., default=False)
    attachments : List 

class EmailAgent:
    def __init__(self):
        pass
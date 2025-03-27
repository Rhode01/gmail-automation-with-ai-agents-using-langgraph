from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, AIMessage
from typing import Annotated, TypedDict,List
from operator import add
from pydantic import Field
from langchain_core.tools import tool
import os
from app_backend.app.AI.core.config import client
from ap

class agentState(StateGraph):
    email_content: str 
    has_attachment:bool = Field(..., default=False)
    attachments :List[None]
    to: str = Field(...,description="The email of the person to send the email")
    from_ : str = Field(..., default="me")

class EmailAgent:
    def __init__(self, gmail_base,gmailBaseCrud):
        self.gmail_base = gmail_base
        self.gmail_crud = gmailBaseCrud
        self.model = client
        self.tools = self._register_tools()
        self.model = self.model.bind_tools(self.tools)
        self.graph = self._setup_graph()    
    @tool
    def send_email_tool(self, to: str, subject: str, body: str):
        """Send an email via Gmail API"""
        return self.gmail_crud.create_email(to, subject, body)
    @tool
    def read_email_tool(self, message_id: str):
            """Retrieve specific email details"""
            return self.gmail_crud.read_email(message_id)
    @tool
    def delete_email_tool(self,message_id: str):
        """Move email to trash"""
        return self.gmail_crud.delete_email(message_id)
    @tool()
    def reply_email_tool(self,message_id: str, reply_body: str):
        """Reply to an existing email"""
        return self.gmail_crud.reply_to_email(message_id, reply_body)
    def _register_tools(self):
        return [
            self.send_email_tool,
            self.read_email_tool,
            self.delete_email_tool,
            self.reply_email_tool
        ]

    def _setup_graph(self):
        graph = StateGraph(agentState)
        
        graph.add_node("analyze_email", self.analyze_email)
        graph.add_node("execute_action", self.execute_action)
        
        graph.add_edge("analyze_email", "execute_action")
        graph.add_conditional_edges(
            "execute_action",
            self._determine_next_step,
            {True: "analyze_email", False: END}
        )
        graph.set_entry_point("analyze_email")
        return graph.compile()


    def execute_action(self, state: agentState):
        if state.get("requires_human"):
            return {**state, "status": "Flagged for human review"}
        
        tool_call = state["tool_call"]
        tool = next((t for t in self.tools if t.name == tool_call["name"]), None)
        
        if tool:
            try:
                result = tool.invoke(tool_call["args"])
                return {**state, "tool_response": result}
            except Exception as e:
                return {**state, "error": str(e)}
        return state
    def analyze_email(self, state: agentState):
        try:
            response = self.model.invoke(analysis_prompt)
            tool_call = self._parse_tool_call(response)
            
            return {
                **state,
                "analysis_result": response,
                "tool_call": tool_call
            }
        except Exception as e:
            return {**state, "requires_human": True}
    def call_openaicall_openai(self):
        
        return
    def exists_action(self, state:agentState):
        result = state['message'][-1]
        return len(result.tool_calls)>0
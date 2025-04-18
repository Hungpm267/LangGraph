# import thư viện
from typing import TypedDict, Annotated
from dotenv import load_dotenv
import sqlite3
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

# cài đặt môi trường
load_dotenv()

# kết nối sqlite
sqlite_conn = sqlite3.connect("checkpoint_hung.sqlite", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)

# khởi tạo tools
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

# khởi tạo LLM và tích hợp các công cụ
llm = ChatGroq(model="llama-3.1-8b-instant", verbose=True)
llm_with_tools = llm.bind_tools(tools=tools)

# Định nghĩa cấu trúc trạng thái và chức năng chính
class BasicChatState(TypedDict): 
    messages: Annotated[list, add_messages]

class state(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState): 
    return {
        "messages": [llm_with_tools.invoke(state["messages"])]
    }

def tools_router(state: BasicChatState):
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
        return "tool_node"
    else: 
        return END
    

# Cài đặt các node và biểu đồ trạng thái
tool_node = ToolNode(tools=tools)
graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", tools_router)
graph.add_edge("tool_node", "chatbot")

# cấu hình và biên dịch biểu đồ trạng thái
config = {"configurable": {
    "thread_id": 123
}}
app = graph.compile(checkpointer=memory)

# vòng lặp chính
while True: 
    user_input = input("User: ")
    if user_input in ["exit", "end"]:
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        }, config=config)

        print("AI: " + result["messages"][-1].content)
        print("Tool calls: " + str(result["messages"][-1].tool_calls))
        print("==========================")
        print("State: " + str(result))
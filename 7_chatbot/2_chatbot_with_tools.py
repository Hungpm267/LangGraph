from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

load_dotenv()

class BasicChatBot(TypedDict):
    messages: Annotated[list, add_messages]

search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

llm = ChatGroq(model="llama-3.1-8b-instant", verbose = True)

llm_with_tools = llm.bind_tools(tools=tools)


# ví dụ tiếp:
# state = {
#     "messages": [
#         HumanMessage(content="Chào bạn"),
#         AIMessage(content="Xin chào! Tôi là trợ lý ảo của bạn."),
#         HumanMessage(content="Bạn có thể tìm giúp tôi thông tin về Python không?")
#     ]
# }
def chatbot_cua_hung(state: BasicChatBot):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])], 
    }




# ví dụ:
# state["messages"] = [
#     HumanMessage(content="Chào bạn, bạn tên là gì?"),
#     AIMessage(content="Tôi là trợ lý ảo của bạn."),
#     HumanMessage(content="Bạn có thể tìm thông tin về Elon Musk không?"),
#     AIMessage(content="Chờ tôi tìm kiếm một chút..."),
#     HumanMessage(content="Ngoài ra, hôm nay ở Hà Nội có mưa không?")
# ]

def tools_router(state: BasicChatBot):
    last_message = state["messages"][-1]

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else: 
        return END
    

tool_node = ToolNode(tools=tools)

graph = StateGraph(BasicChatBot)

graph.add_node("chatbot", chatbot_cua_hung)
graph.add_node("tool_node", tool_node)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", tools_router)
graph.add_edge("tool_node", "chatbot")

app = graph.compile()

while True: 
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })

        print(f"AI: {result['messages'][-1].content}")





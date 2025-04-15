# # con bot này không có tool, memory. chúng ta sẽ học graph stream method. chat looping, use free llama model

# TypedDict: Định nghĩa dictionary với kiểu cụ thể cho từng key.
# Annotated: Thêm metadata vào kiểu dữ liệu, dùng cho framework xử lý thêm thông tin đặc biệt.

from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
from langchain_groq import ChatGroq # ==> pip install langchain-groq


from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant")

class State_cua_bot(TypedDict):
    messages: Annotated[list, add_messages] # messages là key với kdl là list

def chatbot(state: State_cua_bot):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(State_cua_bot)

graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

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
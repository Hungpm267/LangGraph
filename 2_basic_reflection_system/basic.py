# pip install langgraph
from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain

# messageGraph là 1 class dùng để điều phối luồng tin nhắn giữa các node

load_dotenv()

REFLECT = "reflect"
GENERATE = "generate"
dothi =  MessageGraph()

def generate_node(state):
    return generation_chain.invoke({"messages": state})
def reflect_node(messages):
    response = reflection_chain.invoke({"messages": messages})
    return [HumanMessage(content=response.content)]

dothi.add_node(REFLECT, reflect_node)
dothi.add_node(GENERATE, generate_node)
dothi.set_entry_point(GENERATE)
def should_continue(state):
    if(len(state)> 4):
        return END
    return REFLECT
dothi.add_conditional_edges(GENERATE, should_continue)
dothi.add_edge(REFLECT, GENERATE)

ungdung = dothi.compile()
print(ungdung.get_graph().draw_mermaid())
ungdung.get_graph().print_ascii()

response = ungdung.invoke(HumanMessage(content = "AI Agent taking over content creation"))

print(response)
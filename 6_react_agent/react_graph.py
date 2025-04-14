from dotenv import load_dotenv

load_dotenv()

from langchain_core.agents import AgentFinish, AgentAction
from langgraph.graph import END, StateGraph

from nodes import reason_node, act_node
from react_state import AgentState

REASON_NODE = "reason_node"
ACT_NODE = "act_node"

def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT_NODE


graph = StateGraph(AgentState)

graph.add_node(REASON_NODE, reason_node)
graph.set_entry_point(REASON_NODE)
graph.add_node(ACT_NODE, act_node)


graph.add_conditional_edges(
    REASON_NODE,
    should_continue,
)

graph.add_edge(ACT_NODE, REASON_NODE)

app = graph.compile()

result = app.invoke(
    {
        "input": "How many days ago was the latest SpaceX launch?", 
        "agent_outcome": None, 
        "intermediate_steps": []
    }
)

print(result["agent_outcome"].return_values["output"], "final result")



# 4. react_graph.py
# File này xây dựng đồ thị trạng thái để điều khiển luồng xử lý ReAct:

# Định nghĩa hàm should_continue để quyết định liệu agent đã hoàn thành hay cần tiếp tục
# Tạo StateGraph với AgentState làm kiểu trạng thái
# Thêm các nút reason_node và act_node vào đồ thị
# Thiết lập reason_node làm điểm khởi đầu
# Thêm các cạnh có điều kiện để quyết định luồng:

# Nếu agent_outcome là AgentFinish: kết thúc
# Nếu không: chuyển đến act_node


# Thêm cạnh từ act_node quay lại reason_node để tạo vòng lặp
# Biên dịch đồ thị thành ứng dụng thực thi được
# Thực thi ứng dụng với câu hỏi "How many days ago was the latest SpaceX launch?"
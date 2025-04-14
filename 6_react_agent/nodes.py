from dotenv import load_dotenv

from agent_reason_runable import react_agent_runnable, tools
from react_state import AgentState

load_dotenv()

def reason_node(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}


def act_node(state: AgentState):
    agent_action = state["agent_outcome"]
    
    # Extract tool name and input from AgentAction
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    # Find the matching tool function
    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break
    
    # Execute the tool with the input
    if tool_function:
        if isinstance(tool_input, dict):
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)
    else:
        output = f"Tool '{tool_name}' not found"
    
    return {"intermediate_steps": [(agent_action, str(output))]}



# File này định nghĩa các nút xử lý trong luồng ReAct:

# reason_node: Gọi agent để suy luận bước tiếp theo dựa trên trạng thái hiện tại
# act_node: Thực hiện công cụ được chỉ định bởi agent và cập nhật các bước trung gian

# Tìm công cụ phù hợp với tên công cụ từ agent_action
# Thực thi công cụ với đầu vào được cung cấp
# Trả về kết quả dưới dạng bước trung gian
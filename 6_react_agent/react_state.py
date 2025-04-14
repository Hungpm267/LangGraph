import operator
from typing import Annotated, TypedDict, Union

from langchain_core.agents import AgentAction, AgentFinish

class AgentState(TypedDict):
    input: str
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]




# File này định nghĩa cấu trúc trạng thái của agent:

# AgentState là một TypedDict chứa:

# input: Câu hỏi hoặc yêu cầu của người dùng (string)
# agent_outcome: Kết quả từ agent, có thể là AgentAction (hành động tiếp theo) hoặc AgentFinish (kết quả cuối) hoặc None
# intermediate_steps: Danh sách các bước trung gian đã thực hiện, mỗi bước là một tuple gồm (hành động, kết quả)
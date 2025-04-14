from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import tool, create_react_agent
import datetime
from langchain_community.tools import TavilySearchResults
from langchain import hub

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = TavilySearchResults(search_depth="basic")
react_prompt = hub.pull("hwchase17/react") #Lệnh hub.pull("hwchase17/react") sẽ tải một prompt template có tên "hwchase17/react" từ LangChain Hub.


tools = [get_system_time, search_tool]

react_agent_runnable = create_react_agent(tools=tools, llm=llm, prompt=react_prompt)


# File này khởi tạo các thành phần cơ bản của ReAct agent:

# Sử dụng mô hình ChatGoogleGenerativeAI với model "gemini-1.5-flash"
# Định nghĩa một tool get_system_time để lấy thời gian hiện tại theo định dạng cụ thể
# Thêm tool TavilySearchResults để tìm kiếm thông tin trên web
# Tải ReAct prompt từ LangChain Hub
# Khởi tạo ReAct agent sử dụng các tools, LLM và prompt đã cấu hình
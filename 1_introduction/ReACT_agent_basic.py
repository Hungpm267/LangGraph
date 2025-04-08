# pip install langchain langchain_community langchain-google-genai python-dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.agents import initialize_agent, tool
from dotenv import load_dotenv
import datetime
load_dotenv()

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = TavilySearchResults(search_depth = "basic")
tools = [search_tool, get_system_time]
llm = ChatGoogleGenerativeAI(model = "gemini-1.5-flash")
my_agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose = True)


messages = SystemMessage(content = "you are helpful ai assistant, your name is Phạm Công Đặc")
chat_history = []
chat_history.append(messages)
while (True):
    userinput = input("You: ")
    if (userinput.lower() == "exit"):
        break
    chat_history.append(HumanMessage(content=userinput))
    response = my_agent.invoke(userinput)
    print(f"AI response: {response['output']}")
    chat_history.append(AIMessage(content=response['output']))
from langchain.agents import create_agent
from dotenv import load_dotenv 
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

load_dotenv(override=True)


@tool
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = init_chat_model(model="deepseek-chat", model_provider="deepseek")

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)


mcp_client = MultiServerMCPClient(
    {
        "amap-maps": {
              "command": "cmd",
              "args": [
                "/c",
                "npx",
                "-y",
                "@amap/amap-maps-mcp-server"
              ],
              "env": {
                "AMAP_MAPS_API_KEY": "你注册的高德地图api key"
              },
              'transport': 'stdio'
            }
    }
)




conversation = [
    SystemMessage("You are a helpful assistant"),
    HumanMessage("what is the weather in sf.")
]

# Run the agent
result = agent.invoke(
    {"messages": conversation}
)

print(result)
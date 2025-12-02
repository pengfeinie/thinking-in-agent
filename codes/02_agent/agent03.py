from langchain.agents import create_agent
from dotenv import load_dotenv 
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool
from pydantic import BaseModel, Field
load_dotenv(override=True)


class GetWeatherQuery(BaseModel):
    '''Get the current weather in a given location'''
    location: str = Field(description="The city and state, e.g. San Francisco, CA")
    country: str = Field(description="The country of the city and state, e.g. China, USA")


@tool(args_schema=GetWeatherQuery)
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


print(f'''
    name: {get_weather.name},
    description: {get_weather.description},
    arguments: {get_weather.args}
''')

model = init_chat_model(model="deepseek-chat", model_provider="deepseek")


agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

print(result)
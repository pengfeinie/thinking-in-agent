from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
import os

# 启用LangChain追踪
os.environ["LANGSMITH_TRACING"] = "true"
# 设置LangChain API密钥
os.environ["LANGCHAIN_API_KEY"] = "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"
# 这里输入在langsmith中创建的项目的名字
os.environ["LANGCHAIN_PROJECT"] = "default"
# 设置LangChain API端点地址
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# 从环境变量中获取 API 密钥
openai_api_key = os.getenv("OPENAI_API_KEY")

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=openai_api_key,
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

# 定义 ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistant who is good at {ability}. Response in 200 words or fewer."
        ),
        MessagesPlaceholder(variable_name="history"),  # 历史消息占位符
        ("human", "{input}")  # 用户输入
    ]
)

# 将 prompt 和 chat 组合成一个 runnable
runnable = prompt | chat

# 用于存储会话历史的字典
store = {}

# 获取会话历史的函数
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 创建 RunnableWithMessageHistory
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",  # 用户输入的键
    history_messages_key="history"  # 历史消息的键
)

# 第一次调用
response = with_message_history.invoke(
    {"ability": "math", "input": "余弦是什么意思?"},  # 输入
    config={"configurable": {"session_id": "abc123"}}  # 会话 ID
)
print(response.content)

# 第二次调用
response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},  # 输入
    config={"configurable": {"session_id": "abc123"}}  # 会话 ID
)
print(response.content)

# 第三次调用
response = with_message_history.invoke(
    {"ability": "math", "input": "什么?"},  # 输入
    config={"configurable": {"session_id": "abc456"}}  # 会话 ID
)
print(response.content)
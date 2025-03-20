from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
import uvicorn
from pydantic import BaseModel

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAI

# 从环境变量中获取 API 密钥
openai_api_key = os.getenv("OPENAI_API_KEY")
# 启用LangChain追踪
os.environ["LANGSMITH_TRACING"] = "true"
# 设置LangChain API密钥
os.environ["LANGCHAIN_API_KEY"] = "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"
# 这里输入在langsmith中创建的项目的名字
os.environ["LANGCHAIN_PROJECT"] = "default"
# 设置LangChain API端点地址
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# 初始化 ChatOpenAI 实例
chat = ChatOpenAI(
    model="deepseek-chat",
    openai_api_key=openai_api_key,
    openai_api_base="https://api.deepseek.com",
    streaming=False
)

prompt = PromptTemplate.from_template(template="你是一个{name}, 帮我起一个具有{country}特色的{sex}名字.")
messages = prompt.format(name="算命大师", country="法国", sex="女孩")

output_parser = StrOutputParser()

chain = chat | output_parser

app = FastAPI(title="我的Langchain服务", version="v10")


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


# 定义请求体模型
class NameRequest(BaseModel):
    name: str
    country: str
    sex: str

app = FastAPI(title="我的Langchain服务", version="v10")

@app.post("/generate_name/")
async def generate_name(request: NameRequest):
    try:
        # 使用提取的参数调用模型
        prompt = PromptTemplate.from_template(template="你是一个{name}, 帮我起一个具有{country}特色的{sex}名字.")
        messages = prompt.format(name=request.name, country=request.country, sex=request.sex)
        response = chain.invoke(messages)
        return {"generated_name": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 添加 LangChain 路由
add_routes(app, chat | StrOutputParser(), path="/chain")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
from openai import OpenAI
from dotenv import load_dotenv 
from langchain.chat_models import init_chat_model

load_dotenv(override=True)



model = init_chat_model(model="deepseek-chat", model_provider="deepseek")
question = "你好，请你介绍一下你自己。"
result = model.invoke(question)
print(result.content)

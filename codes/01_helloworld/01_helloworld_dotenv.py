import os
from dotenv import load_dotenv 
load_dotenv(override=True)

deepSeek_api_key = os.getenv("DEEPSEEK_API_KEY")
print(deepSeek_api_key)  # 可以通过打印查看

#!/usr/bin/env python3
"""
改进版的智能天气查询程序
支持函数调用和直接天气查询两种模式
"""

import os
import json
import re
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
import requests

# 加载.env文件
load_dotenv()

# API 配置
OPENWEATHER_API_BASE = os.getenv("OPENWEATHER_API_BASE")
OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
USER_AGENT = os.getenv("OPEN_WEATHER_USER_AGENT")
openai_api_key = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://api.deepseek.com")
MODEL = os.getenv("MODEL", "deepseek-chat")

# 函数定义
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The name of the location to get the weather for."
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "The unit of temperature, defaults to celsius."
                }
            },
            "required": ["location"]
        }
    }
]

def extract_location_from_query(query: str) -> Optional[str]:
    """从查询中提取城市名称"""
    # 常见城市名称模式
    patterns = [
        r'(北京|上海|广州|深圳|杭州|南京|苏州|成都|重庆|武汉|西安|天津|郑州|长沙|沈阳|青岛|大连|宁波|厦门|福州|昆明|贵阳|南宁|海口|石家庄|太原|长春|哈尔滨|合肥|南昌|济南)',
        r'(纽约|伦敦|巴黎|东京|悉尼|新加坡|首尔|莫斯科|柏林|罗马|马德里|洛杉矶|旧金山|芝加哥|多伦多|温哥华|墨尔本|奥克兰|香港|台北|澳门)',
        r'([A-Za-z\s]+)(?:的)?天气'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(1).strip()
    
    return None

def get_current_weather(location: str, unit: str = "celsius") -> str:
    """获取当前天气信息"""
    if not location:
        return "请提供有效的城市名称"
    
    url = f"{OPENWEATHER_API_BASE}?q={location}&appid={OPEN_WEATHER_API_KEY}&units=metric&lang=zh_cn"
    
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            temperature = data['main']['temp']
            description = data['weather'][0]['description']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            city_name = data.get('name', location)
            
            if unit == "fahrenheit":
                temperature = temperature * 9/5 + 32
                temp_unit = "℉"
            else:
                temp_unit = "℃"
            
            return (f"📍 {city_name} 天气信息:\n"
                   f"🌡️  当前温度: {temperature:.1f}{temp_unit}\n"
                   f"☁️  天气状况: {description}\n"
                   f"💧 湿度: {humidity}%\n"
                   f"💨 风速: {wind_speed} m/s")
        else:
            return f"❌ 无法获取 {location} 的天气信息，请检查城市名称是否正确"
            
    except requests.exceptions.RequestException as e:
        return f"❌ 网络请求失败: {e}"
    except Exception as e:
        return f"❌ 获取天气信息时出错: {e}"

def get_ai_response(client, user_query: str) -> str:
    """获取AI响应，尝试使用函数调用"""
    try:
        # 首先尝试函数调用
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": user_query}],
            functions=functions,
            function_call="auto",
            timeout=30
        )
        
        message = response.choices[0].message
        
        if message.function_call and message.function_call.name == "get_current_weather":
            arguments = json.loads(message.function_call.arguments)
            location = arguments.get("location")
            unit = arguments.get("unit", "celsius")
            return get_current_weather(location, unit)
        
        # 如果没有函数调用，返回普通响应
        return message.content if message.content else "抱歉，我没有理解您的查询"
        
    except Exception as e:
        # 如果函数调用失败，尝试直接提取城市名称
        print(f"函数调用失败: {e}")
        location = extract_location_from_query(user_query)
        if location:
            return get_current_weather(location)
        else:
            return "抱歉，我无法识别您要查询的城市名称。请明确指定城市，例如：'北京天气怎么样？'"

def main():
    """主程序"""
    print("🌤️  智能天气查询程序")
    print("=" * 40)
    print("输入 '退出', 'quit', 或 'exit' 来退出程序")
    print("=" * 40)
    
    try:
        client = OpenAI(api_key=openai_api_key, base_url=BASE_URL)
    except Exception as e:
        print(f"❌ 初始化API客户端失败: {e}")
        return
    
    while True:
        try:
            user_input = input("\n💬 请输入您的查询: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['退出', 'quit', 'exit']:
                print("👋 再见！")
                break
            
            print("\n" + "=" * 40)
            response = get_ai_response(client, user_input)
            print(response)
            print("=" * 40)
            
        except KeyboardInterrupt:
            print("\n👋 程序已退出")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    main()

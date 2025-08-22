#!/usr/bin/env python3
"""
简单测试脚本用于验证程序基本功能
"""

import os
import sys
from dotenv import load_dotenv
import requests

# 加载环境变量
load_dotenv()

def test_basic_functionality():
    """测试基本功能"""
    print("=" * 50)
    print("基本功能测试")
    print("=" * 50)
    
    # 测试OpenWeather API
    print("1. 测试OpenWeather API...")
    OPENWEATHER_API_BASE = os.getenv("OPENWEATHER_API_BASE")
    OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    USER_AGENT = os.getenv("OPEN_WEATHER_USER_AGENT")
    
    if not all([OPENWEATHER_API_BASE, OPEN_WEATHER_API_KEY]):
        print("❌ OpenWeather API配置缺失")
        return False
    
    url = f"{OPENWEATHER_API_BASE}?q=Beijing&appid={OPEN_WEATHER_API_KEY}&units=metric&lang=zh_cn"
    try:
        response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ OpenWeather API正常")
            print(f"   温度: {data['main']['temp']}℃")
            print(f"   天气: {data['weather'][0]['description']}")
            print(f"   湿度: {data['main']['humidity']}%")
            print(f"   风速: {data['wind']['speed']} m/s")
        else:
            print(f"❌ OpenWeather API错误: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ OpenWeather API异常: {e}")
        return False
    
    # 测试DeepSeek API密钥
    print("\n2. 测试DeepSeek API配置...")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key and openai_api_key.startswith("sk-"):
        print("✅ DeepSeek API密钥格式正确")
    else:
        print("❌ DeepSeek API密钥格式错误或缺失")
        return False
    
    # 测试环境变量完整性
    print("\n3. 测试环境变量完整性...")
    required_vars = [
        "OPENAI_API_KEY",
        "OPEN_WEATHER_API_KEY", 
        "OPENWEATHER_API_BASE",
        "OPEN_WEATHER_USER_AGENT"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺失的环境变量: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ 所有必需环境变量已配置")
    
    print("\n" + "=" * 50)
    print("✅ 基本功能测试通过！")
    print("程序配置正确，可以正常运行。")
    print("=" * 50)
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)

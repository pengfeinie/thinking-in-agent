# 01_function_calling_weather - 智能天气查询程序

## 项目概述

01_function_calling_weather 是一个基于 DeepSeek API 和 OpenWeather API 的智能天气查询程序。它使用函数调用功能，能够智能识别用户关于天气的查询，并自动调用 OpenWeather API 获取实时天气信息。

## 功能特点

- 使用 DeepSeek 大模型进行自然语言理解
- 自动识别天气相关的查询
- 调用 OpenWeather API 获取实时天气数据
- 支持中文和英文查询
- 交互式命令行界面

## API Key 获取指南

### 1. 获取 DeepSeek API Key

1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
2. 注册或登录您的账户
3. 进入 API Keys 管理页面
4. 点击 "Create new secret key" 生成新的 API Key
5. 复制生成的 API Key 备用

### 2. 获取 OpenWeather API Key

1. 访问 [OpenWeatherMap 官网](https://openweathermap.org/api)
2. 注册或登录您的账户
3. 进入 API Keys 页面
4. 点击 "Generate" 生成新的 API Key
5. 复制生成的 API Key 备用

## 安装和配置

### 环境要求

- Python 3.12+
- pip 包管理工具

### 安装依赖

```bash
pip install -e .
```

### 配置环境变量

编辑 `.env` 文件，填入您的 API Key。如果还没有 `.env` 文件，可以复制 `.env.example` 作为模板：

```bash
cp .env.example .env
```

然后编辑 `.env` 文件：

```
# DeepSeek API 配置
OPENAI_API_KEY=您的_DeepSeek_API_Key_在这里

# OpenWeather API 配置
OPEN_WEATHER_API_KEY=您的_OpenWeather_API_Key_在这里
OPENWEATHER_API_BASE=https://api.openweathermap.org/data/2.5/weather
OPEN_WEATHER_USER_AGENT=weather-app/1.0

# DeepSeek 基础配置
BASE_URL=https://api.deepseek.com
MODEL=deepseek-chat
```

## 启动程序

```bash
python main.py
```

## 使用方法

1. 启动程序后，在命令行中输入您的查询
2. 程序会自动识别是否是关于天气的查询
3. 如果是天气查询，会调用 OpenWeather API 获取实时数据
4. 其他查询会由 DeepSeek 模型直接回答

### 示例查询

- "北京天气怎么样？"
- "What's the weather like in Shanghai?"
- "今天深圳的温度是多少？"
- "纽约的天气情况"
- "exit" (退出程序)

### 交互示例

```
Enter your query: 北京天气怎么样？
当前温度为：25℃
天气状况：晴间多云
湿度：65%
风速：3.5 m/s
--------------------------------------------------

Enter your query: What's the weather in Tokyo?
Current temperature: 18℃
Weather condition: light rain
Humidity: 80%
Wind speed: 2.1 m/s
--------------------------------------------------
```

## 预期效果

- **智能识别**: 程序能够智能识别用户是否在询问天气信息
- **实时数据**: 对于天气查询，返回 OpenWeather API 提供的实时天气数据
- **多语言支持**: 支持中英文天气查询和回答
- **详细信息**: 提供温度、天气状况、湿度、风速等详细信息
- **其他查询**: 对于非天气相关的查询，使用 DeepSeek 模型进行智能回答

## 退出程序

输入以下任意命令即可退出程序：
- "退出"
- "quit" 
- "exit"

## 技术栈

- Python 3.12+
- OpenAI Python SDK (兼容 DeepSeek API)
- Requests (HTTP 请求)
- python-dotenv (环境变量管理)

## 项目结构

```
01_function_calling_weather/
├── main.py          # 主程序文件
├── pyproject.toml   # 项目配置和依赖
├── .env            # 环境变量配置文件
├── README.md       # 项目说明文档
└── build/          # 构建输出目录
```

## 注意事项

1. 请妥善保管您的 API Key，不要泄露给他人
2. 确保网络连接正常，能够访问 DeepSeek 和 OpenWeather API
3. 某些地区可能需要科学上网才能正常访问 API
4. OpenWeather API 有调用频率限制，请合理使用

tools = [
    {
        "type": "function",
        "function": {
            "name": "image",
            "description": "接受用户的描述并生成一张图片",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "对需要生成的图片的描述，如：“生成一张动漫风格的风景照”"}
                },
                "required": ["prompt"],
                "strict": True
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mc_ping",
            "description": "当用户需要查询并发送了一个Minecraft Java版服务器ip地址/域名时，此工具可以查询一个Minecraft Java版服务器的信息（在线人数、版本、状态等信息）",
            "parameters": {
                "type": "object",
                "properties": {
                    "ip": {"type": "string", "description": "这个服务器的ip地址/域名，如：“www.hypixel.net”或“104.17.17.42”"}
                },
                "required": ["ip"],
                "strict": True
            }
        }
    }
]




'''
示例：
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取指定城市的实时天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "城市名，如：北京"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["city"]
        }
    }
}
'''
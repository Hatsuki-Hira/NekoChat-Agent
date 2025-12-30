import os
import json
from typing import AsyncGenerator


import using_openaiapi
from small_tools import temp_memory, date, agent_tools, mc_info


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROMPT = open(os.path.join(BASE_DIR, 'prompt.txt'), 'r', encoding='utf-8').read()
PROMPT_SMART_ADDON = open(os.path.join(BASE_DIR, 'prompt_smart_addon.txt'), 'r', encoding='utf-8').read()



# 主工作流
async def flow_main(input_content: list) -> AsyncGenerator:
    # 调用ai
    ai = using_openaiapi.StreamProcessor()
    date.get()
    prompt=f'''

*这是你的角色系统设定，请牢牢记住！：
“{PROMPT}”。

*这是你与用户之前的对话历史记录（从前往后按照时间顺序排序，每行开头冒号前的人用来提醒你这句话是谁说的，回复时不要模仿着加上这个人物和冒号，直接打出你要说的话就行）：
“{date.get()}
{temp_memory.get()}”

#markdown支持功能（高亮代码块、表格、列表等）：
若用户有需求，你需要严格按照markdown格式输出，如代码段高亮等功能（在开头的三个反引号后指定语言，比如```python\nprint('hello world')\n```）

#你可以调用所列出来的一些内置的ai agent工具使用，注意你需要先对用户的输入做出反应再调用工具（如聊聊天或回应一下：“正在调用工具！”等等，内容请根据情景自由发挥），如果什么也不说直接调用工具会显得很冷淡

*以上系统设置记住后，直接处理以下用户的输入吧：

'''
    output = ai.get_Qwen3_VL(
        prompt=prompt,
        input_content=input_content,
        tools=agent_tools.tools
    )

    # 传递常规回复文本输出流
    async for i in output:
        yield i

    # 解析调用的工具
    if ai.tool_info:
        for index, call in ai.tool_info.items():
            try:
                full_args = json.loads(call["arguments"])
                print(f"[info] 准备执行工具 {call['name']}，参数：{full_args}")

                if call['name'] == 'image':
                    print('1')

                if call['name'] == 'mc_ping':
                    mcinfo = mc_info.get(full_args['ip'])
                    yield mcinfo
                
            except Exception as e:
                print(f"解析工具参数失败: {e}")
    
    # 打印token使用量
    print(ai.token_info)







'''
#重要！：不要使用内置的思考链逻辑生成推理（<thinking>的内容），请直接生成对话内容

在每一个波浪线 '~' 前添加反斜杠 '\' 转义（即写成 '\~'），使得 Markdown 不会将相邻的波浪线解析为删除线格式。
'''
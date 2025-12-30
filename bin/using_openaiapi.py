from openai import AsyncOpenAI
from typing import AsyncGenerator

from small_tools import temp_memory



client = AsyncOpenAI(
    base_url='https://api.siliconflow.cn/v1',
    api_key=''
)



class StreamProcessor:
    def __init__(self):
        self.token_info = ''
        self.tool_info = {}

    async def get_deepseek_V3_2(self, prompt: str, input_content: list, tools: list) -> AsyncGenerator[str, dict]:
        # 储存输入内容
        for i in input_content:
            if i['type'] == 'text':
                n = ''.join(i['text'])
        temp_memory.add('"用户"：'+ n)

        response = await client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3.2",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": input_content
                }
            ],
            stream=True,
            max_tokens=4096,
            temperature=0.65,  # 严谨细致 0.2~0.8 想象发散
            tools=tools,
            tool_choice='auto',
            extra_body={"enable_thinking": False}
        )

        if response.response.status_code == 200:
            mem_output = []  # 整合常规回复文本，用于储存输出内容
            collected_tool_calls = {}  # 工具调用碎片整合
            # 处理流
            async for chunk in response:
                # print(chunk)
                # 处理文本
                if chunk.choices[0].delta.content:
                    #print(chunk.choices[0].delta.content, end="", flush=True)
                    mem_output.append(chunk.choices[0].delta.content)
                    yield chunk.choices[0].delta.content
                # 处理推理内容
                if chunk.choices[0].delta.reasoning_content:
                    #print(chunk.choices[0].delta.reasoning_content, end="", flush=True)
                    print(f'[info] 推理内容：{chunk.choices[0].delta.reasoning_content}')
                # 处理工具调用碎片
                delta = chunk.choices[0].delta
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        index = tool_call.index
                        if index not in collected_tool_calls:
                            # 初始化这个索引的工具调用信息
                            collected_tool_calls[index] = {
                                "id": tool_call.id,
                                "name": tool_call.function.name,
                                "arguments": ""
                            }
                        # 拼接参数字符串
                        if tool_call.function.arguments:
                            collected_tool_calls[index]["arguments"] += tool_call.function.arguments
                # 接收到末段工具调用碎片时
                if chunk.choices[0].finish_reason == "tool_calls":
                    print(f"[info] 模型调用工具：{collected_tool_calls}")
                    self.tool_info = collected_tool_calls
                # 处理流结束
                if chunk.choices[0].finish_reason:
                    total_token = chunk.usage.total_tokens
                    prompt_tokens = chunk.usage.prompt_tokens
                    completion_tokens = chunk.usage.completion_tokens
                    token_info = {
                        'total': total_token,
                        'upload': prompt_tokens,
                        'download': completion_tokens
                    }
                    self.token_info = f"[Info][Tokens] total:{total_token} ↑{prompt_tokens} ↓{completion_tokens}"

                    temp_memory.add('"你"：'+''.join(mem_output))  # 储存输出内容
                    print('[info] 当前对话流结束')
                    return

        else:
            print(f"请求失败，状态码：{response.response.status_code}")



    async def get_Qwen3_VL(self, prompt: str, input_content: list, tools: list) -> AsyncGenerator[str, dict]:
        # 储存输入内容
        for i in input_content:
            if i['type'] == 'text':
                n = ''.join(i['text'])
        temp_memory.add('"用户"：'+ n)

        response = await client.chat.completions.create(
            model="Qwen/Qwen3-VL-235B-A22B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": input_content
                }
            ],
            stream=True,
            max_tokens=4096,
            temperature=0.65,  # 严谨细致 0.2~0.8 想象发散
            tools=tools,
            tool_choice='auto'
        )

        if response.response.status_code == 200:
            mem_output = []  # 整合常规回复文本，用于储存输出内容
            collected_tool_calls = {}  # 工具调用碎片整合
            # 处理流
            async for chunk in response:
                # 处理常规回复
                if chunk.choices[0].delta.reasoning_content:
                    mem_output.append(chunk.choices[0].delta.reasoning_content)
                    yield chunk.choices[0].delta.reasoning_content
                # 处理工具调用碎片
                delta = chunk.choices[0].delta
                if delta.tool_calls:
                    for tool_call in delta.tool_calls:
                        index = tool_call.index
                        if index not in collected_tool_calls:
                            # 初始化这个索引的工具调用信息
                            collected_tool_calls[index] = {
                                "id": tool_call.id,
                                "name": tool_call.function.name,
                                "arguments": ""
                            }
                        # 拼接参数字符串
                        if tool_call.function.arguments:
                            collected_tool_calls[index]["arguments"] += tool_call.function.arguments
                # 接收到末段工具调用碎片时
                if chunk.choices[0].finish_reason == "tool_calls":
                    print(f"[info] 模型决定调用工具：{collected_tool_calls}")
                    self.tool_info = collected_tool_calls
                # 处理流结束
                if chunk.choices[0].finish_reason:
                    total_token = chunk.usage.total_tokens
                    prompt_tokens = chunk.usage.prompt_tokens
                    completion_tokens = chunk.usage.completion_tokens
                    token_info = {
                        'total': total_token,
                        'upload': prompt_tokens,
                        'download': completion_tokens
                    }
                    self.token_info = f"[Info][Tokens] total:{total_token} ↑{prompt_tokens} ↓{completion_tokens}"

                    temp_memory.add('"你"：'+''.join(mem_output))  # 储存输出内容
                    print('[info] 当前对话流结束')
                    return

        else:
            print(f"请求失败，状态码：{response.response.status_code}")
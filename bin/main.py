from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import base64
import json
from typing import List, Optional, AsyncGenerator

from workflow import flow_main


app = FastAPI()



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "webui/static")
if not os.path.exists(static_path):
    os.makedirs(static_path)
# 静态文件目录，用于临时存放上传的图片或前端资源
app.mount("/static", StaticFiles(directory=static_path), name="static")



async def message_response(user_input: str, uploaded_files: List[UploadFile]) -> AsyncGenerator:
    '''debug代码
    response_parts = []
    
    response_parts.append(f"这是针对 '{user_input}' 的异步回复。\n\n")

    if uploaded_files:
        response_parts.append(f"我收到了 **{len(uploaded_files)}** 张图片：\n")
        for file in uploaded_files:
            response_parts.append(f"- 文件名: `{file.filename}`\n")
            response_parts.append(f"  内容类型: `{file.content_type}`\n")
            response_parts.append(f"  大小: `{file.size / 1024:.2f} KB`\n")
            
            # 也可以在这里保存文件到 static 目录，并在响应中返回一个可访问的URL
            with open(os.path.join(static_path, file.filename), "wb") as f:
                f.write(await file.read())
            response_parts.append(f"""<a href="/static/{file.filename}" target="_blank"><img src="/static/{file.filename}" class="max-w-[400px] max-h-[400px] rounded-lg cursor-zoom-in"></a>\n""")


    response_parts.append("\n```python\nprint('hello world')\n```\n")

    full_response = "".join(response_parts)

    for char in full_response:
        yield f"data: {json.dumps({'content': char})}\n\n"
        await asyncio.sleep(0.01) # 模拟思考
    '''
    input_content = []

    input_content.append({
        "type": "text",
        "text": user_input
        })

    if uploaded_files:
        for file in uploaded_files:
            img_base64 = base64.b64encode(await file.read()).decode('utf-8')
            if file.content_type in ['image/jpeg', 'image/png', 'image/webp']:
                # 保存文件到 static 目录，并传入数据列表
                with open(os.path.join(static_path, file.filename), "wb") as f:
                    f.write(await file.read())
                    f.close()
                input_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{file.content_type};base64,{img_base64}",
                        "detail": "high"
                    }
                })
    
    # 调用api
    output = flow_main(input_content=input_content)
    async for i in output:
        i = i.replace('~', r'\~') # 防止前端渲染波浪线的时候两个波浪线之间的内容变为删除线，强制转义文本
        i = i.replace('\n', '<br>') # html会吞掉换行符
        yield f"data: {json.dumps({'content': i})}\n\n"  # SSE数据块格式，要匹配数据格式！



# 初始页面
@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_file_path = os.path.join(BASE_DIR, "webui/index.html")
    with open(index_file_path, encoding="utf-8") as f:
        return f.read()



# 接收到消息
@app.post("/chat")
async def chat(
    # 参数名必须和前端一样，不然解不了包(
    message: str = Form(default=''), 
    # 使用 File(default=None) 明确告诉 FastAPI 这个字段是可选的，不然会422
    files: Optional[List[UploadFile]] = File(default=None) 
):
    # files 可能是 None，确保它是一个列表
    if files is None:
        files = []
    return StreamingResponse(message_response(message, files), media_type="text/event-stream")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
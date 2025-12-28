# 临时记忆体
CONTEXT_LIST_LENGTH = 10
chat_history = []
for i in range(CONTEXT_LIST_LENGTH):
    chat_history.append('')

def add(element: str):
    for i in range(CONTEXT_LIST_LENGTH-1):
        chat_history[i] = chat_history[i+1]
    chat_history[CONTEXT_LIST_LENGTH-1] = element + '\n'
    # print(f"""[Info][History]{'\n'.join(chat_history)}""")

def get():
    return '\n'.join(chat_history)
from mcstatus import JavaServer


def get(ip: str):
    server = JavaServer.lookup(ip)
    status = server.status()
    onlines = status.players.online
    latency = server.ping()
    try:
        query = server.query()
        return f"当前有{onlines}个玩家在线，服务器延迟为{latency:.1f}ms\n玩家列表如下：{', '.join(query)}\n"
    except:
        return f"当前有{onlines}个玩家在线，服务器延迟为{latency:.1f}ms\n服务器隐藏了详细的玩家名称列表\n"

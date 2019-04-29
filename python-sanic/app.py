from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol

app = Sanic()

@app.websocket('/train')
async def train(request,ws):
  while True:
    data = await ws.recv()
    await ws.send(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)

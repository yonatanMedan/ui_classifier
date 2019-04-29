from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from classifier.dataset import create_dataset
app = Sanic()

@app.websocket('/train')
async def train(request,ws):
  while True:
    data = await ws.recv()
    print(data)
    dataset = create_dataset(data)
    dataset.show_batch(rows=3, figsize=(7, 8))
    await ws.send("dataset created")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)

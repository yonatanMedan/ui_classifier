from sanic import Sanic
from sanic.response import json
from sanic.websocket import WebSocketProtocol
from classifier.dataset import create_dataset
from classifier.train import get_model
app = Sanic()

@app.websocket('/train')
async def train(request,ws):
  while True:
    data = await ws.recv()
    print(data)
    dataBunch = create_dataset(data)
    learn = get_model(dataBunch)
    learn.fit(1)
    dataBunch.show_batch(rows=3, figsize=(7, 8))
    await ws.send("dataset created")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)

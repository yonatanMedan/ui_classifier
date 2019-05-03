from sanic import Sanic
from sanic.response import json
import json as JSON
from sanic.websocket import WebSocketProtocol
from classifier.dataset import create_dataset
from classifier.train import get_model
from WSEvents.WSEventEmitter import  WSEventEmitter
app = Sanic()

def handleFolder(emitter,folder):
  print("folder event")
  return emitter.ws.send("dataset created")

@app.websocket('/train')
async def train(request,ws):
  emitter = WSEventEmitter(ws)
  dataSetFolderSubject = emitter.get_subject("dataset_folder")
  dataSetFolderSubject.subscribe(handleFolder,scheduler)
  await handleFolder(emitter,folder)
  await emitter.start_event_loop()

  #while True:
  #  socket_event = await ws.recv()
  #  emitter.emit(event_type,data)
  #  print(data)
  #  dataBunch = create_dataset(data)
  #  learn = get_model(dataBunch)
  #  learn.fit(1)
  #  dataBunch.show_batch(rows=3, figsize=(7, 8))
  #  await ws.send("dataset created")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)

from sanic import Sanic
from sanic.response import json
import json as JSON
from sanic.websocket import WebSocketProtocol
# from classifier.dataset import create_dataset
# from classifier.train import get_model
from rx.subjects import Subject
from rx.concurrency.mainloopscheduler import AsyncIOScheduler
from rx import operators as ops
from rx import from_future
from functools import partial
from WSEvents.WSEventEmitter import  WSEventEmitter
from classifier.Learner import Learner
import asyncio
app = Sanic()

async def handleFolder(emitter,folder):
  print("folder event")
  return await emitter.ws.send("dataset created")

@app.websocket('/train')
async def train(request,ws):
  scheduler = AsyncIOScheduler()
  emitter = WSEventEmitter(ws)
  dataSetFolderSubject = emitter.get_subject("dataset_folder")
  dataSetFolderSubject.pipe(
    ops.flat_map(
      lambda folder:
        from_future(asyncio.create_task(handleFolder(emitter,folder)))
    )
  ).subscribe(lambda x: print("hello"),scheduler=scheduler)
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

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
  learner = Learner.from_folder(folder)
  print("dataset_created")
  await emitter.send("dataset_created","None")
  return learner

async def train_stage_1(emitter,learner:Learner):
  learner.train_start(1)
  await emitter.send("train_stage_1")
  return learner

async def train_stage_2(emitter,learner:Learner):
  learner.train_unfreezed(1)
  await emitter.send("train_stage_2")
  return learner


def to_observable(corutin):
  return from_future(asyncio.create_task(corutin))
@app.websocket('/train')
async def train(request,ws):
  contex = {}
  scheduler = AsyncIOScheduler()
  emitter = WSEventEmitter(ws)
  dataSetFolderSubject = emitter.get_subject("dataset_folder")
  trainFirstStage = emitter.get_subject("train_stage_1")
  trainUnfreezed = emitter.get_subject("train_unfreezed")

  dataSetFolderSubject.pipe(
    ops.flat_map(
      lambda folder:
        to_observable(handleFolder(emitter,folder))
    ),
    ops.do_action(lambda learner:contex.__setitem__("learner",learner)),
    ops.flat_map(lambda event:
        trainFirstStage
    ),
    ops.flat_map(
      lambda event:
        to_observable(train_stage_1(emitter,contex["learner"]))
    ),
    ops.flat_map(
      lambda learner:
        trainUnfreezed
    ),
    ops.flat_map(
      lambda event:
        to_observable(train_stage_2(emitter,contex["learner"]))
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

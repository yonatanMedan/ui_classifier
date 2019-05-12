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
from controller import LearnerController
app = Sanic()
async def handleFolder(folder,emitter):
  learner = Learner.from_folder(folder)
  print("dataset_created")
  await emitter.send("dataset_created","dataset_created")
  return learner

async def train_stage_1(event,emitter,contex):
  learner = contex["learner"]
  learner.train_start(1)
  await emitter.send("train_stage_1","train stage 1")
  return learner

async def train_stage_2(event,emitter,contex):
  learner = contex["learner"]
  learner.train_unfreezed(1)
  await emitter.send("train_unfreezed")
  return learner

async def predict(img_path,emitter,contex):
  learner = contex["learner"]
  print(img_path)
  prediction = learner.predict(img_path)
  await emitter.send("photo_predictions",prediction)
  return prediction



def to_observable(corutin):
  return from_future(asyncio.create_task(corutin))

def async_switch_map(corutin,*args,**kwargs):
  return ops.flat_map_latest(lambda event:to_observable(corutin(event,*args,**kwargs)))

@app.websocket('/train')
async def train(request,ws):
  controller = LearnerController(ws)
  await controller.start_init_chains()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)

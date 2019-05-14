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


@app.websocket('/train')
async def train(request,ws):
  controller = LearnerController(ws)
  await controller.start_init_chains()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, protocol=WebSocketProtocol)

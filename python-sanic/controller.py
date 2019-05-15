from WSEvents.WSEventEmitter import  WSEventEmitter
from classifier.Learner import Learner
from rx.subjects import Subject
# from rx.concurrency.mainloopscheduler import AsyncIOScheduler
from rx import operators as ops
from rx import from_future
from asgiref.sync import sync_to_async

import asyncio
def to_observable(corutin):
    return from_future(asyncio.create_task(corutin))

def async_switch_map(corutin,*args,**kwargs):
    return ops.flat_map_latest(lambda event:to_observable(corutin(event,*args,**kwargs)))


class LearnerController:
    def __init__(self,ws):
        self.emitter = WSEventEmitter(ws)
        self.learner =None
        self.dataSetFolderSubject = self.emitter.get_subject("dataset_folder")
        self.trainFirstStage = self.emitter.get_subject("train_stage_1")
        self.trainUnfreezed = self.emitter.get_subject("train_unfreezed")
        self.predict_one_obs = self.emitter.get_subject("predict_one")
    
    def set_learner(self,learner):
        self.learner=learner

    def get_trained_obs(self):
        return self.dataSetFolderSubject.pipe(
            async_switch_map(self.handleFolder),
            ops.do_action(self.set_learner),
            ops.flat_map_latest(lambda event:self.trainFirstStage),
            async_switch_map(self.train_stage_1),
            ops.share()
        )

    def pipe_train_2(self,obs):
        return obs.pipe(
            ops.flat_map_latest(lambda x:self.trainUnfreezed),
            async_switch_map(self.train_stage_2)
        )
    
    def pipe_predict_one(self,obs):
        return obs.pipe(
        ops.flat_map_latest(
            lambda x:
                self.predict_one_obs
            ),
            async_switch_map(self.predict)
        )

    async def start_init_chains(self):
        train_obs = self.get_trained_obs()
        self.pipe_train_2(train_obs).subscribe()
        self.pipe_predict_one(train_obs).subscribe()
        await self.emitter.start_event_loop()

    async def handleFolder(self,folder):
        self.learner = Learner.from_folder(folder,self.emitter)
        print("dataset_created")
        await self.emitter.send("dataset_created","dataset_created")
        return self.learner

    async def train_stage_1(self,event):
        self.learner.train_start(1)
        # self.learner.train_start(1)
        await self.emitter.send("train_stage_1","train stage 1")
        return self.learner

    async def train_stage_2(self,event):
        self.learner.train_unfreezed(1)
        await self.emitter.send("train_unfreezed")
        return self.learner

    async def predict(self,img_path):
        print(img_path)
        prediction = self.learner.predict(img_path)
        await self.emitter.send("photo_predictions",prediction)
        return prediction




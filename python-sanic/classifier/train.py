from fastai.vision import models,cnn_learner,error_rate,accuracy
from fastai.basic_train import  LearnerCallback,dataclass,nn
from rx.subjects import Subject
import asyncio
class EventSubjects(LearnerCallback):
    def __init__(self,emitter,*args,**kwargs):
      print("init EventSubjects")
      super().__init__(*args,**kwargs)
      self.batch_end_subject = emitter.get_subject("batch_end_subject")
      self.emitter = emitter
    def on_batch_end(self, **kwargs):
        print("batch end")
        asyncio.create_task(self.emitter.send("batch_end","batch_end"))
        self.batch_end_subject.on_next("batch end")

def get_learner(data):
  return cnn_learner(data, models.resnet34,metrics=[error_rate,accuracy])

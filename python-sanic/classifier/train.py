from fastai.vision import models,cnn_learner,error_rate,accuracy
from fastai.basic_train import LearnerCallback,dataclass,nn
from rx.subjects import Subject
@dataclass
class ProgressCallback(LearnerCallback):
    batch_end_subject:Subject
    def on_batch_end(self, **kwargs):
        print("batch end")
        self.batch_end_subject.on_next("batch end")

def get_learner(data):
  return cnn_learner(data, models.resnet34,metrics=[error_rate,accuracy])

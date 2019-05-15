
from .train import get_learner,EventSubjects
from .dataset import create_data_bunch
from fastai.vision import ImageDataBunch,open_image
from rx.subjects import Subject
from functools import partial
from fastai.callbacks.tensorboard import LearnerTensorboardWriter
import pdb
class Learner:
    def __init__(self,dataBunch:ImageDataBunch,get_learner_func=None,emitter=None):
        self.data = dataBunch
        if get_learner_func is None:
            get_learner_func = get_learner

        self.learner = get_learner_func(self.data)
        self.learner.callback_fns.append(partial(LearnerTensorboardWriter, base_dir=self.data.path, name='UIlearner'))
        self.learner.callback_fns.append(partial(EventSubjects,emitter))
        self.batch_end_subject = Subject()

    @classmethod
    def from_folder(cls,folder,emitter=None):
        dataBunch = create_data_bunch(folder)
        return cls(dataBunch,emitter=emitter)

    def train_start(self,n=1):
        self.learner.freeze()
        self.learner.fit_one_cycle(n)
        self.save('stage1')

    def train_unfreezed(self,n=1):
        self.learner.unfreeze()
        self.learner.fit_one_cycle(n,max_lr=slice(1e-7,1e-5))
        self.save("stage2")

    def save(self,name="model"):
        self.learner.save(name)

    def predict(self,img_path):
        img = open_image(img_path)
        pred = self.learner.predict(img)
        return {
            "prediction":str(pred[0]),
            "prob":float(pred[2][pred[1]])
        }


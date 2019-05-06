
from .train import get_learner
from .dataset import create_data_bunch
from fastai.vision import ImageDataBunch
class Learner:
    def __init__(self,dataBunch:ImageDataBunch,get_learner_func=None):
        self.data = dataBunch
        if get_learner_func is None:
            get_learner_func = get_learner

        self.learner = get_learner_func(self.data)

    @classmethod
    def from_folder(cls,folder):
        dataBunch = create_data_bunch(folder)
        return cls(dataBunch)

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
    


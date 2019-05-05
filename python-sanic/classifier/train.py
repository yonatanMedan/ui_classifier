from fastai.vision import models,cnn_learner,error_rate,accuracy

def get_learner(data):
  return cnn_learner(data, models.resnet34,metrics=[error_rate,accuracy])

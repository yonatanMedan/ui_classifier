from fastai.vision import models,cnn_learner,error_rate,accuracy

def get_model(data):
  return cnn_learner(data, models.resnet34,metrics=[error_rate,accuracy])

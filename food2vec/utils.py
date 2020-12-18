from tensorflow.keras.callbacks import Callback
from tensorflow.keras import backend as K 
import math

class FoodDataPaths:
    image_data_path = ''
    food_dir_path = ''
    tfr_path = ''
    model_save_path = ''
    models_dir = ''
    test_image_path = ''


    @classmethod
    def make_img_food_path(cls, img_data_path, food_dir_path):
        cls.image_data_path = img_data_path
        cls.food_dir_path = food_dir_path
    
    @classmethod
    def make_tfr_path(cls, tfr_path):
        cls.tfr_path = tfr_path

    @classmethod
    def make_model_save_path(cls, model_save_path):
        cls.model_save_path = model_save_path
    
    @classmethod
    def make_models_dir(cls, models_dir):
        cls.models_dir = models_dir

    @classmethod
    def make_test_image_path(cls, test_image_path):
        cls.test_image_path = test_image_path


class CosineAnnealingScheduler(Callback):
    """Cosine annealing scheduler.
    """

    def __init__(self, T_max, eta_max, eta_min=0, verbose=0):
        super(CosineAnnealingScheduler, self).__init__()
        self.T_max = T_max
        self.eta_max = eta_max
        self.eta_min = eta_min
        self.verbose = verbose

    def on_epoch_begin(self, epoch, logs=None):
        if not hasattr(self.model.optimizer, 'lr'):
            raise ValueError('Optimizer must have a "lr" attribute.')
        lr = self.eta_min + (self.eta_max - self.eta_min) * (1 + math.cos(math.pi * epoch / self.T_max)) / 2
        K.set_value(self.model.optimizer.lr, lr)
        if self.verbose > 0:
            print('\nEpoch %05d: CosineAnnealingScheduler setting learning '
                  'rate to %s.' % (epoch + 1, lr))

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        logs['lr'] = K.get_value(self.model.optimizer.lr)

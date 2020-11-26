import os
from glob import glob
import tensorflow as tf
from utils import FoodDataPaths


class Modelselect:

    '''
    EfficientNetB0 => eb0
    EfficientNetB1 => eb1
    ...

    MobileNetv1 => mv1
    MobileNetv2 => mv2
    Xception => x
    NASNetmobile => nasm
    NASNetlarge => nasl
    Densenet => dn
    '''


    def __init__(self, model_name, image_size, class_num):
        self.model_name = model_name
        self.image_size = image_size 
        self.class_num = class_num


    def model(self):
        model_parameters = {
            'input_shape': (self.image_size, self.image_size, 3),
            'include_top': False,
            'weights': 'imagenet',
        }
        if self.model_name =='eb0':
            base_model = tf.keras.applications.EfficientNetB0(**model_parameters)
        elif self.model_name =='eb1':
            base_model = tf.keras.applications.EfficientNetB1(**model_parameters)
        elif self.model_name =='eb2':
            base_model = tf.keras.applications.EfficientNetB2(**model_parameters)
        elif self.model_name =='eb3':
            base_model = tf.keras.applications.EfficientNetB3(**model_parameters)
        elif self.model_name =='eb4':
            base_model = tf.keras.applications.EfficientNetB4(**model_parameters)
        elif self.model_name =='eb5':
            base_model = tf.keras.applications.EfficientNetB5(**model_parameters)
        elif self.model_name =='eb6':
            base_model = tf.keras.applications.EfficientNetB6(**model_parameters)
        elif self.model_name =='eb7':
            base_model = tf.keras.applications.EfficientNetB7(**model_parameters)
        elif self.model_name =='mv1':
            base_model = tf.keras.applications.MobileNet(**model_parameters)
        elif self.model_name =='mv2':
            base_model = tf.keras.applications.MobileNetV2(**model_parameters)
        elif self.model_name =='x':
            base_model = tf.keras.applications.Xception(**model_parameters)
        elif self.model_name =='nasm':
            base_model = tf.keras.applications.NASNetMobile(**model_parameters)
        elif self.model_name =='nasl':
            base_model = tf.keras.applications.NASNetLarge(**model_parameters)
        elif self.model_name =='d121':
            base_model = tf.keras.applications.DenseNet121(**model_parameters)
        elif self.model_name == 'res50':
            base_model = tf.keras.applications.ResNet50(**model_parameters)


        flatten_layer = tf.keras.layers.Flatten()
        dense_layer = tf.keras.layers.Dense(512, activation='relu')
        prediction_layer = tf.keras.layers.Dense(self.class_num)

        model = tf.keras.Sequential([
            base_model,
            flatten_layer,
            dense_layer,
            prediction_layer
        ])

        print(model.summary())
        return model


class ModelselectForTest(FoodDataPaths):
    
    models = {}

    def __init__(self, model_num = 5):
        self.model_num = model_num

    def __str__(self):
        self._models_dict()
        return str(self.models)

    def _make_models_dirs(self):
        return glob(os.path.join(self.models_dir, "*"))

    def _make_model_list(self):
        model_list = os.listdir(self.models_dir)
        model_list = [ x for x in model_list if "ipynb" not in x]
        model_list = list(map(lambda x : '_'.join(x.split('/')[-1].split('_')[:-1]), model_list))
        return model_list

    def _models_dict(self):
        model_list = self._make_model_list()
        for idx, m in enumerate(model_list):
            self.models[idx] = m

    def load_model(self):
        self._models_dict()
        model_name = self.models[self.model_num]
        models_dirs = self._make_models_dirs()
        
        for model_dir in models_dirs:
            check_dir = os.path.join(self.models_dir, model_name+'_checkpoint')
            if check_dir == model_dir:
                target = check_dir
                break

        trained_models = glob(os.path.join(target, "*-*-*.h5"))
        trained_models = sorted(trained_models, key=lambda x : os.path.basename(x).split('-')[-1], reverse=True)  # 정확도 기준, 내림차순 정렬
        print('Model 불러오는 중...')
        target_model = tf.keras.models.load_model(trained_models[0]) # 가장 정확도가 높은 모델을 load
        print(f'불러온 모델의 경로 : {trained_models[0]}')
        print('완료\n')

        return target_model

    
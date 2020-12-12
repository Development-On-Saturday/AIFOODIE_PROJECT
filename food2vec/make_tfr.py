import tensorflow as tf 
import numpy as np 
from utils import FoodDataPaths
from glob import glob
from tqdm import tqdm
import os 



class DataListChecker(FoodDataPaths):
    '''
    Data 목록 check
    : food_dir_path => data들이 들어있는 디렉토리
    '''
    image_label = {}
    
    def make_dict(self):
        food_lst =os.listdir(self.food_dir_path)
        for idx, name  in enumerate(food_lst):
            self.image_label[name] = idx
        return self.image_label
    
    def __call__(self):
        return self.make_dict()


class FoodTFrecord(FoodDataPaths):

    def __len__(self):
        return len(glob(self.image_data_path))

    @staticmethod
    def _bytes_feature(value):
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy() # BytesList won't unpack a string from an EagerTensor.
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    @staticmethod
    def _float_feature(value):
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

    @staticmethod
    def _int64_feature(value):
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    def make_tfr(self):
        image = DataListChecker()
        image_label = image()
        _writer = tf.io.TFRecordWriter(self.tfr_path)
        print('TFRecord를 생성합니다...... \n 생성중 ......')

        _n = 0
        for path in tqdm(glob(self.image_data_path)):
            image = open(path, 'rb').read()

            class_name = path.split('/')[-2]
            label = image_label[class_name]

            feature = {
                'image' : FoodTFrecord._bytes_feature(image),
                'label' : FoodTFrecord._int64_feature(label),
            }

            example = tf.train.Example(features=tf.train.Features(feature=feature))
            _writer.write(example.SerializeToString())
            _n += 1
        _writer.close()
        print(f'The number of file : {_n}개')
        print(f"{self.tfr_path}에 TFRecord 생성")

    def read_tfr(self):
        raw_image_dataset = tf.data.TFRecordDataset(self.tfr_path)
        image_feature_description = {
            'image' : tf.io.FixedLenFeature([], tf.string),
            'label' : tf.io.FixedLenFeature([], tf.int64)
        }

        def _parse_image_function(example_proto):
            return tf.io.parse_single_example(example_proto, image_feature_description)

        parsed_image_dataset = raw_image_dataset.map(_parse_image_function)
        return parsed_image_dataset


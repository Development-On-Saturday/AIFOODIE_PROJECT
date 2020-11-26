import tensorflow as tf
import os
import cv2
import matplotlib.pyplot as plt
import tensorflow_datasets as tfds
from functools import partial
from albumentations import (
    Compose, HorizontalFlip, Rotate, ShiftScaleRotate, VerticalFlip,
    RandomSizedCrop, CenterCrop, Resize
)
AUTOTUNE = tf.data.experimental.AUTOTUNE

transforms = Compose([
            Resize(224,224),
            RandomSizedCrop(min_max_height=(195, 220), height=224, width=224, p=0.5),
            Rotate(limit=60, p=0.5),
            HorizontalFlip(p=0.5),
        ])

class DataPreprocessing():
    
    AUTOTUNE = tf.data.experimental.AUTOTUNE

    def __init__(self, tfr_filepath, image_size, batch_size, buffer_size, dataset_size):
        self.image_size = image_size
        self.batch_size = batch_size
        self.buffer_size = buffer_size
        self.image_shape = (image_size, image_size, 3)
        self.dataset_size = dataset_size
        
        # tfr파일 경로를 받아온다. 
        self.tfr_filepath = tfr_filepath
        
        # tfr파일을 불러온다.
        self.raw_image_dataset = tf.data.TFRecordDataset(self.tfr_filepath)
        
        # Create a dictionary describing the features.
        self.image_feature_description = {
                'image' : tf.io.FixedLenFeature([], tf.string),
                'label': tf.io.FixedLenFeature([], tf.int64),
            }
    
    #아래 두 함수는 한 묶음으로 tfr파일의 정보를 feature dict에 맞게 변환, 할당한다.
    def _parse_image_function(self,example_proto):
            return tf.io.parse_single_example(example_proto, self.image_feature_description)
        
    def _parsed_image_dataset(self):
        paresd_img_data = self.raw_image_dataset.map(self._parse_image_function)
        return paresd_img_data
    
    def train_valid_split(self):
        train_size = int(0.8 * self.dataset_size)
        val_size = int(0.2 * self.dataset_size)
    
        dataset = self._parsed_image_dataset()
        dataset = dataset.shuffle(self.buffer_size)
        
        train_ds = dataset.take(train_size)
        valid_ds = dataset.skip(train_size)
        valid_ds = dataset.take(val_size)
        
        return train_ds, valid_ds
    
    def data_alb(self, dataset, is_train):
        ds_alb = dataset.map(partial(self.process_data, image_size=self.image_size, is_train=is_train), num_parallel_calls=self.AUTOTUNE)
        if is_train:
            print(f"{is_train} in data_alb func")
            ds_alb = ds_alb.map(partial(self.set_shapes, img_shape=self.image_shape), num_parallel_calls=self.AUTOTUNE)
            ds_alb = ds_alb.repeat()
           
        ds_alb = ds_alb.batch(self.batch_size)
        ds_alb = ds_alb.prefetch(self.AUTOTUNE)
        return ds_alb
    
    # Augmentation을 적용시키는 함수이다.
    def aug_fn(self, image, img_size):
        data = {"image":image}
        aug_data = transforms(**data)
        aug_img = aug_data["image"]
        #aug_img = tf.cast(aug_img/255.0, tf.float32)
        aug_img = tf.image.resize(aug_img, size=[img_size, img_size])
        return aug_img

    # tfr에 담겨있는 img, label을 받아와서 img만 aug_fn함수에 전달한 후
    # aug_img, label을 다시 반환하여 데이터쌍을 유지한다.
    def process_data(self, data, image_size, is_train=True):
        image = data["image"]
        label = data["label"]
        image = tf.image.decode_image(image, channels=3, expand_animations=False)
        
        if is_train:
            image = tf.numpy_function(func=self.aug_fn, inp=[image, image_size], Tout=tf.float32)
            
        else:
            print(f"process_data else {is_train}")
            image = tf.image.resize(image, (224, 224))
            
        label = tf.one_hot(label, 30)
        return image, label
    
    # 최종적으로 데이터의 shape을 정의해준다.
    def set_shapes(self, img, label, img_shape):
        img.set_shape(img_shape)
        return img, label
    
    def view_image(self, ds):
        image, label = next(iter(ds)) # extract 1 batch from the dataset
        image = image.numpy()
        label = label.numpy()
        
        image = image/255.0

        fig = plt.figure(figsize=(22, 22))
        for i in range(20):
            ax = fig.add_subplot(4, 5, i+1, xticks=[], yticks=[])
            ax.imshow(image[i])
            ax.set_title(f"Label: {tf.argmax(label[i])}")
            
    def decode_img(self, _valid):
        image = _valid['image']
        label = _valid['label']

        image = tf.image.decode_image(image, channels=3, expand_animations = False)
        #image = tf.cast(image/255, dtype=tf.float32)
        image = tf.image.resize(image, (224, 224))

        label = tf.one_hot(label, 30)

        return image, label
    
    def __call__(self):
        train, valid = self.train_valid_split()
        train = self.data_alb(train, is_train = True)
        valid = valid.map(self.decode_img).batch(self.batch_size)
        
        return train, valid
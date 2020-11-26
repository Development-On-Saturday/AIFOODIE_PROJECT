from tqdm import tqdm
import tensorflow as tf 
import numpy as np 
from glob import glob
from utils import FoodDataPaths

np.random.seed(123)

class Prediction(FoodDataPaths):

    def _load_image(self, path, img_size) :
        img = tf.io.read_file(path)
        img = tf.image.decode_image(img, channels=3, expand_animations=False)
        img = tf.image.resize(img, (img_size, img_size))

        label = int(path.split('/')[-2].split('_')[-1])
        return img, label

    def predict_test(self, model, img_size, nums=0):
        test_image_path = glob(self.test_image_path)
        correct = 0
        if nums == 0:
            img_paths = test_image_path
        else:
            img_paths = np.random.choice(test_image_path, nums, replace=False)

        for img_path in tqdm(img_paths):
            img, label = self._load_image(img_path, img_size)
            img = img[np.newaxis, :, :]
            pred = int(np.argmax(model.predict(img)))

            if pred == label:
                correct += 1

        print(f'정확도 : {round(correct / len(img_paths), 4) * 100}%')


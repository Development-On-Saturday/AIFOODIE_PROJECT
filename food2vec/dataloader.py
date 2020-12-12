import tensorflow as tf 
from make_tfr import FoodTFrecord

tf.random.set_seed(123)

class FoodDataLoader_with_TFRecord(FoodTFrecord):

    def __init__(self, image_size, label_num, batch_size, train_valid_rate):
        self.parsed_image_dataset = self.read_tfr()
        self.image_size = image_size
        self.batch_size = batch_size
        self.train_valid_rate = train_valid_rate
        # 추후에 class 숫자가 확정되면 사라질 변수
        self.label_num = label_num

    def _decode_img(self, data):
        image = data['image']
        label = data['label']

        image = tf.image.decode_image(image, channels=3, expand_animations = False)
        image = tf.image.resize(image, (self.image_size,self.image_size))

        label = tf.one_hot(label, self.label_num)
        return image, label

    def food_tf_dataset(self, tfr_size):

        train_size = int(float(self.train_valid_rate[0]) * tfr_size)
        val_size = int(float(self.train_valid_rate[1]) * tfr_size)

        dataset = self.parsed_image_dataset
        dataset = dataset.shuffle(30000)
        # train
        train_ds = dataset.take(train_size)
        train_ds = train_ds.map(self._decode_img)
        train_ds = train_ds.batch(self.batch_size)
        train_ds = train_ds.repeat()
        train_ds = train_ds.prefetch(tf.data.experimental.AUTOTUNE)

        valid_ds = dataset.skip(train_size)
        valid_ds = dataset.take(val_size)
        valid_ds = valid_ds.map(self._decode_img)
        valid_ds = valid_ds.batch(self.batch_size)

        return train_ds, valid_ds
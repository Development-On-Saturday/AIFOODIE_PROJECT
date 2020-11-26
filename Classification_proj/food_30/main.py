import argparse
import math
import tensorflow as tf
from models import Modelselect, ModelselectForTest
from dataloader import FoodDataLoader_with_TFRecord
from make_tfr import FoodTFrecord
from utils import FoodDataPaths,CosineAnnealingScheduler
from prediction import Prediction

tf.random.set_seed(123)

def to_bool(x):
    if x.lower() in ['true','t']:
        return True
    elif x.lower() in ['false','f']:
        return False
    else:
        raise argparse.ArgumentTypeError('Bool 값을 넣으세요')


if __name__ =="__main__":

    print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
    tf.debugging.set_log_device_placement(True)
    tf.config.list_physical_devices("GPU")

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=['tfr', 'train', 'test'], help="TFRecord 만들기 or 모델 학습 or 모델 테스트")
    parser.add_argument("--food_dir_path", type=str, default='./', help="각 음식들의 폴더가 저장되어 있는 상위 디렉토리")
    parser.add_argument("--model_name", type=str, choices=["eb0","eb1","eb2","eb3","eb4","eb5","eb6","eb7","mv1","mv2","x","nasm","nasl", "d121", "res50"],default="eb0")
    parser.add_argument("--model_save_dir", type=str, default='./')
    parser.add_argument("--models_dir", type=str, default='./', help="테스트를 위해 학습이 끝난 모델이 저장된 디렉토리")
    parser.add_argument("--tfr_path", type=str, default='./')
    parser.add_argument("--test_image_path", type=str, default='./')
    parser.add_argument("--tfr_size", type=int)
    parser.add_argument("--image_data_path", type=str, default='./')
    parser.add_argument("--batch_size", type=int)
    parser.add_argument("--image_size", type=int)
    parser.add_argument("--label_num", type=int)
    parser.add_argument("--train_valid_rate" ,nargs="+")
    parser.add_argument("--epochs", type=int)
    parser.add_argument("--patience", type=int)
    parser.add_argument("--test_model_num", type=int)
    parser.add_argument("--test_size", type=int, default=0)
    parser.add_argument("--test_model_check", type=to_bool, default='false')
    
    args = parser.parse_args()

    # path 입력
    food_paths = FoodDataPaths()
    food_paths.make_img_food_path(args.image_data_path, args.food_dir_path)
    food_paths.make_model_save_path(args.model_save_dir)
    food_paths.make_tfr_path(args.tfr_path)
    food_paths.make_models_dir(args.models_dir)
    food_paths.make_test_image_path(args.test_image_path)

    # parameters 
    batch_size = args.batch_size
    image_size = args.image_size
    label_num = args.label_num
    epochs = args.epochs
    train_valid_rate = args.train_valid_rate


    if args.test_model_check:
         model_list = ModelselectForTest()
         print(model_list)
    else:
        # tfr 만들기
        if args.mode =='tfr':
            tfr_make = FoodTFrecord()
            tfr_make.make_tfr()
        
        # model 학습
        elif args.mode == "train":
            mc_dir_path = food_paths.model_save_path
            if mc_dir_path == './':
                raise NotADirectoryError("model 폴더에 저장하세요")

            size = args.tfr_size
            dataloader = FoodDataLoader_with_TFRecord(image_size, label_num, batch_size, train_valid_rate)
            train, valid = dataloader.food_tf_dataset(size)

            model = Modelselect(model_name=args.model_name, image_size=image_size, class_num=label_num)
            model = model.model()

            steps = math.floor(size/batch_size)
            cos = CosineAnnealingScheduler(T_max=steps, eta_max=6e-4, eta_min=3e-5)
            es = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=args.patience)
            mc = tf.keras.callbacks.ModelCheckpoint(
                filepath=mc_dir_path+'{epoch}-{val_loss:.2f}-{val_accuracy:.2f}.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1,
            )
            model.compile(
                optimizer=tf.keras.optimizers.Adam(),
                loss = tf.keras.losses.CategoricalCrossentropy(),
                metrics=['accuracy']
            )

            history = model.fit(
                train,
                epochs=epochs,
                validation_data=valid,
                steps_per_epoch= size / batch_size,
                callbacks=[es, mc, cos],
                batch_size=batch_size,
            )
        elif args.mode == "test":
            model_instance = ModelselectForTest(args.test_model_num)
            model = model_instance.load_model()

            pred = Prediction()
            
            test_size = args.test_size
            # model test
            pred.predict_test(model, image_size, test_size)

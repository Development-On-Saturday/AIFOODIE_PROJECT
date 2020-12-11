import shutil
import json
import os
from PIL import Image
import numpy as np
from django.shortcuts import reverse, redirect, render
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from .models import Food

with open("./data/label_info.json", 'r', encoding="UTF-8-sig") as f:
    label_info = json.load(f)

with open("./data/aifoodie_hashtags.json", "r", encoding="UTF-8-sig") as f:
    hashtags = json.load(f)

class ClassifierView(TemplateView):
    template_name = "foods/classifier.html"
    
def predictImage(request):
    fileObj = request.FILES["filePath"]
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    base_path = "./uploads/"
    model = load_model("./models/new_model.h5")

    base_name = os.path.basename(filePathName)
    testimage = base_path + base_name
    food_image = Image.open(testimage)
    food_image = food_image.convert("RGB")
    food_image = food_image.resize((360, 360))
    food_image = np.array(food_image)
    x = food_image[np.newaxis, :, :, :]
    pred = model.predict(x)
    index = np.argmax(pred[0])
    predictedLabel = label_info[str(index)]
    # shutil.move(testimage, move_path + media_file)
    try:
        if hashtags[str(index)]:
            # 몇 개의 해시태그를 뽑을까?
            num = np.random.randint(3, len(hashtags[str(index)]))
            hashtag =np.random.choice(hashtags[str(index)], num, replace=False)
            print(hashtag)
    except IndexError:
        pass
    food = Food(name=predictedLabel)
    food.save()

    context = {"filePathName": filePathName, "predictedLabel": predictedLabel, "hashtags" : hashtag}
    return render(request, "foods/classifier_r.html", context)


def FoodPlaceSearch(request):
    search = Food.objects.order_by("-pk")[0].name
    context = {"search" : search}
    return render(request, "foods/search_place.html", context)
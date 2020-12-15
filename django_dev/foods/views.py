import json
import re
import os
from PIL import Image
import numpy as np
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from tensorflow.keras.models import load_model
from .models import Food
from users.models import User

with open("./data/label_info.json", "r", encoding="utf-8-sig") as f:
    label_info = json.load(f)

with open("./data/aifoodie_hashtags.json", "r", encoding="utf-8-sig") as f:
    hashtags = json.load(f)


class ClassifierView(TemplateView):
    template_name = "foods/classifier.html"


def predictImage(request):
    fileObj = request.FILES["filePath"]

    # 한글 파일명 영어로 바꿔주기
    if re.findall("[ㄱ-ㅎ가-힣]", fileObj.name) != []:
        tail = os.path.splitext(fileObj.name)[1]
        nums = np.random.randint(0, 9999999)
        fileObj.name = "image_file_" + str(nums) + tail

    users = User.objects.get(pk=request.user.pk)
    # DB
    food = Food(name="", image=fileObj, user=users)
    
    search = Food.objects.order_by("-pk")[0].image
    model = load_model("./models/new_model.h5")

    testimage = search.file
    food_image = Image.open(testimage)
    food_image = food_image.convert("RGB")
    food_image = food_image.resize((360, 360))
    food_image = np.array(food_image)
    x = food_image[np.newaxis, :, :, :]
    pred = model.predict(x)
    index = np.argmax(pred[0])
    predictedLabel = label_info[str(index)]

    try:
        if hashtags[str(index)]:
            # 몇 개의 해시태그를 뽑을까?
            num = np.random.randint(3, len(hashtags[str(index)]))
            hashtag = np.random.choice(hashtags[str(index)], num, replace=False)
            print(hashtag)
    except IndexError:
        pass

    food.name = predictedLabel
    food.save()
    context = {
        "filePathName": search.url,
        "predictedLabel": predictedLabel,
        "hashtags": hashtag,
    }

    return render(request, "foods/classifier_r.html", context)


def FoodPlaceSearch(request):
    search = Food.objects.order_by("-pk")[0].name
    context = {"search": search}
    return render(request, "foods/search_place.html", context)

class HistoryView(ListView):
    model = Food
    template_name = "foods/history.html"
    context_object_name = "history"

    def get_queryset(self):
        return Food.objects.filter(user=self.request.user).order_by("-created")
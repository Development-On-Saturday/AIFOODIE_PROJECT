import shutil
import os
from PIL import Image
import numpy as np
from django.shortcuts import reverse, redirect, render
from django.core.files.storage import FileSystemStorage
from django.views.generic import TemplateView
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from .models import Food


label_info = {
    "0": "갈비구이",
    "1": "갈비탕",
    "2": "갈치구이",
    "3": "갈치조림",
    "4": "감자탕",
    "5": "계란말이",
    "6": "고추튀김",
    "7": "곰탕_설렁탕",
    "8": "곱창전골",
    "9": "김밥",
    "10": "김치볶음밥",
    "11": "김치전",
    "12": "김치찌개",
    "13": "닭볶음탕",
    "14": "된장찌개",
    "15": "만두",
    "16": "비빔밥",
    "17": "삼겹살",
    "18": "새우볶음밥",
    "19": "생선전",
    "20": "소세지볶음",
    "21": "양념치킨",
    "22": "육개장",
    "23": "육회",
    "24": "제육볶음",
    "25": "짬뽕",
    "26": "찜닭",
    "27": "파전",
    "28": "피자",
    "29": "후라이드치킨",
}


class ClassifierView(TemplateView):
    template_name = "foods/classifier.html"


def predictImage(request):
    fileObj = request.FILES["filePath"]
    fs = FileSystemStorage()
    filePathName = fs.save(fileObj.name, fileObj)
    filePathName = fs.url(filePathName)
    base_path = "./uploads/"
    move_path = "./uploads/foods/"
    model = load_model("./models/new_model.h5")

    if os.listdir(base_path)[0] == "foods":
        media_file = os.listdir(base_path)[1]
    else:
        media_file = os.listdir(base_path)[0]
    testimage = base_path + media_file

    food_image = Image.open(testimage)
    food_image = food_image.convert("RGB")
    food_image = food_image.resize((360, 360))
    food_image = np.array(food_image)

    x = food_image[np.newaxis, :, :, :]
    pred = model.predict(x)
    predictedLabel = label_info[str(np.argmax(pred[0]))]

    shutil.move(testimage, move_path + media_file)
    # context = {"filePathName": filePathName, "predictedLabel": predictedLabel}
    # return render(request, "foods/classifier.html", context)
    print(predictedLabel)
    return redirect(reverse("foods:classifier"))


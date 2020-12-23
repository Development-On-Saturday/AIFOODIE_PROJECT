# 음식 이미지 인식, 분류 연구 및 MLOps 퍼블리싱 프로젝트 (AIFOODIE)

## Screen Shot
![AIFOODIE](https://user-images.githubusercontent.com/48716219/102978823-76eae700-4548-11eb-920a-6085e040c702.png)
![screenshot](https://user-images.githubusercontent.com/48716219/102978652-2d020100-4548-11eb-88ea-6ef64c5f1295.jpg)



[Web🌐](https://aifoodieheroku.herokuapp.com/)

[Demo Video ![youtube](https://user-images.githubusercontent.com/48716219/102975581-a77c5200-4543-11eb-893b-45c19273e964.png) 
](https://youtu.be/buMXyjiqjrk)

## 프로젝트 요약


이 프로젝트는 모두의 연구소에서 주관하는 인공지능 혁신학교 AIFFEL의 3조에서 수행한 마지막 해커톤 프로젝트 입니다.

100개의 한식데이터에 대해서 음식을 분류를 주제로 하였고 분류하는 모델 뿐만 아니라 DCGAN, Grad-CAM, T-SNE를 활용해서 시각화 시도도 해보았습니다.

- 구성원 (옆에는 깃허브 아이콘, 블로그 아이콘 등으로 버튼하나씩 만들기)

    김윤경(팀 리딩) [![GitHub-Mark-32px](https://user-images.githubusercontent.com/48716219/102974622-31c3b680-4542-11eb-815d-70efcdeb2e75.png)](https://github.com/YesicaKim)


    신태양(프론트엔드)[![GitHub-Mark-32px](https://user-images.githubusercontent.com/48716219/102974622-31c3b680-4542-11eb-815d-70efcdeb2e75.png)](https://github.com/tyshin94) [![nb30](https://user-images.githubusercontent.com/48716219/102975150-f37ac700-4542-11eb-9606-9414ed89f0de.png)](https://blog.naver.com/tyshin94)


    정민채(MLOps, 백엔드)[![GitHub-Mark-32px](https://user-images.githubusercontent.com/48716219/102974622-31c3b680-4542-11eb-815d-70efcdeb2e75.png)](https://github.com/Jungminchae)

    변호윤(Deep Learning)[![GitHub-Mark-32px](https://user-images.githubusercontent.com/48716219/102974622-31c3b680-4542-11eb-815d-70efcdeb2e75.png)](https://github.com/hybyun0121)

    이재호(Deep Learning)[![GitHub-Mark-32px](https://user-images.githubusercontent.com/48716219/102974622-31c3b680-4542-11eb-815d-70efcdeb2e75.png)](https://github.com/ljh415) [![nb30](https://user-images.githubusercontent.com/48716219/102975150-f37ac700-4542-11eb-9606-9414ed89f0de.png)](https://blog.naver.com/ab415)


- 사용한 데이터 : [AI Hub 한식 이미지데이터베이스](https://www.aihub.or.kr/aidata/130)

    학습된 클래스 : 100 (총 150개중 100개만 선정)

- 사용한 구조 : EfficientNet + GAP + BN + Dense

    ![01](https://user-images.githubusercontent.com/48716219/102970888-afd08f00-453b-11eb-8066-26724c042828.png)

- Test 결과

    ![02](https://user-images.githubusercontent.com/48716219/102970908-b959f700-453b-11eb-931a-1c8c78388f8c.png)

- Grad-CAM (./Classification_proj/notebooks/CAM_Class.ipynb)

    후라이드치킨, 양념치킨에 대한 Grad-CAM

    ![03](https://user-images.githubusercontent.com/48716219/102970948-cb3b9a00-453b-11eb-8987-af585f45ef78.png)

- DCGAN _ 육개장

    ![gan](https://user-images.githubusercontent.com/48716219/102970988-e0182d80-453b-11eb-9fc8-fdb76b766a1b.gif)



## 프로젝트 기간


- 2020.09.17 ~ 2020.12.21 (3개월)



## 사용한 기술 스택


- Git
- Python
- TensorFlow, Keras
- HTML, CSS, JavaScript
- Gougle Cloud, AWS, Heroku



## 실행방법


> 가상환경을 새로 만드시고, 새로운 가상환경에서 실행해 주세요

```bash
# initial setting
$ git clone https://github.com/Development-On-Saturday/AIFOODIE_PROJECT.git
$ cd AIFOODIE
$ python run.py

# or manual
$ cd django_dev
$ pip install -r requirments.txt
$ python manage.py migrate
$ python manage.py runserver
```

> 이미 Library를 설치하였고 **서버만** 실행시킬 때

```bash
$ python run.py -r True
```



## Code Details
<details>
    <summary> Click to toggle contents of details </summary>
- `./Classification_proj`

    - ```/notebooks``` : Notebook 파일
    - ```/food_30``` : python 파일

- `./django_dev`
    
    - 로컬 개발용 코드 [배포용 코드는 따로 저장]
    - ```/core```
        - ```/models.py```
            - Data가 생성된 시간을 기록해주는 모델 클래스
        - ```/views.py```
            - 홈페이지를 나타내주는 HomeView
                - CBV - Class Based View
                - TemplateView
    - ```/foods```
        - ```/model.py``` : 음식을 올린 유저, 모델이 추론한 이름, 이미지 저장 위치를 저장하는 모델 클래스
        - ```/view.py```
            - ```ClassifierView``` - Classifier 페이지를 보여주는 TemplateView
            - ```predictimage``` - 사용자에게 받은 이미지를 모델에 넣어 추론하는 View
                - FBV - Function Based View
            - ```FoodPlaceSearch``` - 모델 추론 값을 지도 검색에 검색어로 보내주는 View
                - FBV - Function Based View
            - ```HistoryView``` - 유저가 추론한 히스토리를 최근 순서대로 볼 수 있는 View
                - CBV - Class Based View
                - ListView
    
    - ```/photos```
        - ```/models.py```
            - 프로젝트 결과물이 주제별로 저장될 Album 클래스
            - 앨범에 들어가 사진들이 저장될 Photo 클래스
        - ```/views.py```
            - Album ListView : 프로젝트 주제별 Album을 리스트로 보여주는 View
            - Album DetailView : 특정 Album에 대한 디테일한 디스크립션을 보여주는 View
            - Photo DetailView : Album에 있는 사진을 자세하게 설명하는 View
- `./food2vec`

    호윤님이 설명

- `./reports`

    발표자료 보관
</details>

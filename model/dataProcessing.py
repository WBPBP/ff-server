import sys;
import json
import numpy as np
import pandas as pd;
import copy
import random
from walkData import normalGait, out_toedGait, in_toedGait, craneGait, elevenGait, diseasePrediction
# walkData.py 파일에 기준이 되는 데이터들이나 comment를 적어놓았어요!

# 정적족저압의 결과를 분석하여 comment를 반환해주는 함수입니다.
def analysisStaticPressureResult(verticalWeightBias_Left, verticalWeightBias_Right, horizontalWeightBias, heelPressureDifference):
    comment, leftState = verticalBalanceCheck_Left(verticalWeightBias_Left)
    comment += verticalBalanceCheck_Right(verticalWeightBias_Right, leftState)
    comment += horizontalBalanceCheck(horizontalWeightBias)
    comment += scoliosisDiagnosis(heelPressureDifference)
    return comment

# 왼발의 앞/뒤꿈치 중 어느 쪽으로 중심이 더 쏠렸는지 판단
def verticalBalanceCheck_Left(verticalWeightBias_Left):
    comment = "양 발 중 왼발은 "
    if verticalWeightBias_Left < 0.48:
        comment += "무게중심이 앞꿈치보다 뒤꿈치로 쏠려있는 경향이 보입니다."
        leftState = 0
    elif verticalWeightBias_Left < 0.52:
        comment += "무게중심이 뒤꿈치보다 앞꿈치로 쏠려있는 경향이 보입니다."
        leftState = 1
    else:
        comment += "무게가 왼발에 앞/뒤꿈치에 고르게 분포해있어 안정적으로 보입니다."
        leftState = 2
    return comment, leftState

# 오른발의 앞/뒤꿈치 중 어느 쪽으로 중심이 더 쏠렸는지 판단
def verticalBalanceCheck_Right(verticalWeightBias_Right, leftState):
    if verticalWeightBias_Right < 0.48:
        comment = " 오른발 또한 " if(leftState==0) else " 하지만 오른발은"
        comment += "무게중심이 앞꿈치보다 뒤꿈치로 쏠려있는 경향이 보입니다."
    elif verticalWeightBias_Right < 0.52:
        comment = " 오른발 또한 " if (leftState == 1) else " 하지만 오른발은"
        comment += "무게중심이 뒤꿈치보다 앞꿈치로 쏠려있는 경향이 보입니다."
    else:
        comment = " 오른발 또한 " if (leftState == 2) else " 하지만 오른발은"
        comment += "무게가 왼발에 앞/뒤꿈치에 고르게 분포해있어 안정적으로 보입니다."
    return comment

# 양 발의 무게중심이 어느 쪽으로 치우쳐져 았는 판단
def horizontalBalanceCheck(horizontalWeightBias):
    comment = ""
    if horizontalWeightBias < 0.48:  # '왼-오'로 계산을 했기 때문에 압력 차값이 0에 가까울수록 몸의 무게중심이 왼발에 치우쳐져 있음
        comment = " 몸의 무게중심은 왼쪽으로 치우쳐져 있는 경향이 보입니다."
    elif horizontalWeightBias < 0.52:  # 압력 차 편향이 1에 가까울수록 몸의 무게중심이 오른발에 치우쳐져 있음
        comment = " 몸의 무게중심은 오른쪽으로 치우쳐져 있는 경향이 보입니다."
    else:  # 압력 차 편향이 0.5에 가까울수록 무게중심이 잘 잡혀있음
        comment = " 몸 전체의 무게중심은 몸무게가 양발에 고르게 분포해있어 몸의 균형은 안정적으로 보입니다."
    return comment  # 몸의 무게중심이 어느쪽으로 치우쳐져 있는지 comment

# 척추측만증을 의심해볼 수 있는지 판단
def scoliosisDiagnosis(heelPressureDifference):
    comment = ""
    if heelPressureDifference > 29: #압력 차이가 기준보다 높은 것들의 수가 전체 개수의 반 이상이면 척추측만증 의심
        comment = " 또한 현재 양쪽 발에 실리는 힘의 차이가 크게 나는 것으로 보아 척추측만증을 의심해볼 수 있습니다."
    return comment

def avgList(list): # 형식이 list인 경우 전체 원소에 대한 평균을 구하는 함수
    return sum(list, 0.0)/len(list)

def walkCheck(leftPressure, rightPressure): # 걸음걸이 습관 파악 및 질병예측을 위한 함수
    left = copy.deepcopy(leftPressure)
    right = copy.deepcopy(rightPressure)
    # 형태를 변화시켜주기 위해 복사해서 사용
    left = np.asarray(left).reshape(12,-1)
    right = np.asarray(right).reshape(12,-1)
    # 해당 값이 아마도 list로 들어올 것같아서 일단 numpy배열 형식으로 변경하였습니다.
    # 또한 원래 12개 센서값들을 10개씩 가지고 있었어서배열의 형태도 [[센서1의 변화값(10)],[센서2의 변화값(10)],[센서3의 변화값(10)],.....] 변경
    nor_mean = []
    out_mean = []
    in_mean = []
    crane_mean = []
    ele_mean = []
    # 상관분석 값들을 저장 list를 선언했습니다.

    normal=normalGait()
    out_toe=out_toedGait()
    in_toe=in_toedGait()
    crane=craneGait()
    ele=elevenGait()
    # 각 걸음걸이 데이터값을 가져오기 위해서 데이터 값이 저장되어있는 class를 선언

    #각 12개 센서에 대해 각 걸음걸이데이터와 피어슨 상관관계분석 진행
    for i in range(12):
        nor_l = pd.DataFrame({"normal_l":normal.getLeft()[i], "ori_l":left[i]})
        corr = nor_l.corr(method='pearson')
        # 상관관계분석 진행
        nor_mean.append(corr.values[0][1])
        # 상관관계분석값 중에서 쓰이는 수만 추출?해서 각 걸음걸이와의 상관계수 배열에 넣기
        nor_r = pd.DataFrame({"normal_r": normal.getRight()[i], "ori_r": right[i]})
        corr = nor_r.corr(method='pearson')
        nor_mean.append(corr.values[0][1])

        out_l = pd.DataFrame({"out_l": out_toe.getLeft()[i], "ori_l": left[i]})
        corr = out_l.corr(method='pearson')
        out_mean.append(corr.values[0][1])
        out_r = pd.DataFrame({"out_r": out_toe.getRight()[i], "ori_r": right[i]})
        corr = out_r.corr(method='pearson')
        out_mean.append(corr.values[0][1])

        in_l = pd.DataFrame({"in_l": in_toe.getLeft()[i], "ori_l": left[i]})
        corr = in_l.corr(method='pearson')
        in_mean.append(corr.values[0][1])
        in_r = pd.DataFrame({"in_r": in_toe.getRight()[i], "ori_r": right[i]})
        corr = in_r.corr(method='pearson')
        in_mean.append(corr.values[0][1])

        crane_l = pd.DataFrame({"crane_l": crane.getLeft()[i], "ori_l": left[i]})
        corr = crane_l.corr(method='pearson')
        crane_mean.append(corr.values[0][1])
        crane_r = pd.DataFrame({"crane_r": crane.getRight()[i], "ori_r": right[i]})
        corr = crane_r.corr(method='pearson')
        crane_mean.append(corr.values[0][1])

        ele_l = pd.DataFrame({"ele_l": ele.getLeft()[i], "ori_l": left[i]})
        corr = ele_l.corr(method='pearson')
        ele_mean.append(corr.values[0][1])
        ele_r = pd.DataFrame({"ele_r": ele.getRight()[i], "ori_r": right[i]})
        corr = ele_r.corr(method='pearson')
        ele_mean.append(corr.values[0][1])
    dic = {0:avgList(nor_mean), 1:avgList(out_mean), 2:avgList(in_mean), 3:avgList(crane_mean), 4:avgList(ele_mean)}
    # 어떤 걸음걸이가 제일 상관있는지를 보기 위해서 dictionary로 선언
    dic_reverse = sorted(dic.items(), reverse=True, key=lambda item:item[1])
    #상관계수에 대해 내림차순 정렬

    percent = (int)((dic[0]+1)*50); #올바른 걸음걸이 척도 계산을 위한 상관계수(-1.0~+1.0)를 percentage(0~100)로 변경
    comment = diseasePrediction() # 각 걸음걸이 comment 및 질병예측 commnet를 가져오기 위한 class선언
    return percent, comment.getComment(dic_reverse[0][0]), dic_reverse[0][0];
    #올바른 걸음걸이 척도, 걸음걸이 comment, 질병 아이콘을 위해서(0~4)값 반환
    #{0:"정상걸음", 1:"팔자걸음", 2:"안짱걸음", 3:"학다리 걸음", 4:"11자 걸음"}

def run(verticalWeightBias_Left, verticalWeightBias_Right, horizontalWeightBias, heelPressureDifference, leftPressure, rightPressure) :
    staticPressureRes = analysisStaticPressureResult(verticalWeightBias_Left, verticalWeightBias_Right, horizontalWeightBias, heelPressureDifference);
    score, gaitComment, diseaseNum = walkCheck(leftPressure, rightPressure)
    dict = {"staticPressureRes": staticPressureRes, "percent": score, "gaitComment": gaitComment, "diseaseNum": diseaseNum}
    print(json.dumps(dict, ensure_ascii=False))
    #return json.dumps(dict)
    #json으로 형식 변환


# 실제 사용시에 입력받을 부분입니다.
'''
json_data=sys.argv[1]
data=json.loads(json_data)
verticalWeightBias_Left = data['verticalWeightBias_Left']
verticalWeightBias_Right = data['verticalWeightBias_Right']
horizontalWeightBias = data['horizontalWeightBias']
heelPressureDifference = data['heelPressureDifference']
leftPressure = data['leftPressure']
rightPressure = data['rightPressure']
'''

# 더미 데이터 생성
verticalWeightBias_Left = random.random()
verticalWeightBias_Right = random.random()
horizontalWeightBias = random.random()
heelPressureDifference = random.randint(0, 60)
leftPressure = []
rightPressure = []
for i in range(120):
    leftPressure.append(random.randint(0, 16))
    rightPressure.append(random.randint(0, 16))

#실행 함수 호출
run(verticalWeightBias_Left, verticalWeightBias_Right, horizontalWeightBias, heelPressureDifference, leftPressure, rightPressure)



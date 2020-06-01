import numpy as np
import pandas as pd;
import copy
import math
from WalkData import normalGait, out_toedGait, in_toedGait, craneGait, elevenGait, diseasePrediction

def avgList(list): # 형식이 list인 경우 전체 원소에 대한 평균을 구하는 함수
    return sum(list, 0.0)/len(list)

def walkCheck(leftPressure, rightPressure): # 걸음걸이 습관 파악 및 질병예측을 위한 함수
    if len(leftPressure)!=120 or len(rightPressure) != 120:
        return 0, "결과가 바르지 못해 분석에 실패하였습니다.", 0
    elif math.isnan(leftPressure[0]) or math.isnan(rightPressure[0]):
        return 0, "조금만 더천천히 걸어주세요!", 0
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
    # 상관분석 값들을 저장 list를 선언

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

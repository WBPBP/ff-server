import numpy as np
import pandas as pd;
import copy
import math
import networkx as nx
from WalkData import normalGait, out_toedGait, in_toedGait, craneGait, elevenGait, diseasePrediction

def avgList(list): # 형식이 list인 경우 전체 원소에 대한 평균을 구하는 함수
    return sum(list, 0.0)/len(list)

def calculateDistance(x1, y1, x2, y2):
    d1 = x2 - x1;
    d2 = y2 - y1;
    return math.sqrt((d1**2)+(d2**2))

def CheckEachSensorChange(leftPressure, rightPressure): # 걸음걸이 습관 파악 및 질병예측을 위한 함수
    left = copy.deepcopy(leftPressure)
    right = copy.deepcopy(rightPressure)
    # 형태를 변화시켜주기 위해 복사해서 사용
    left = np.asarray(left).reshape(10, -1)
    left = left.T
    left = left.tolist()
    right = np.asarray(right).reshape(10, -1)
    right = right.T
    right = right.tolist()
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

    normal_left = copy.deepcopy(normal.getLeft())
    normal_right = copy.deepcopy(normal.getRight())
    out_left = copy.deepcopy(out_toe.getLeft())
    out_right = copy.deepcopy(out_toe.getRight())
    in_left = copy.deepcopy(in_toe.getLeft())
    in_right = copy.deepcopy(in_toe.getRight())
    crane_left = copy.deepcopy(crane.getLeft())
    crane_right = copy.deepcopy(crane.getRight())
    ele_left = copy.deepcopy(ele.getLeft())
    ele_right = copy.deepcopy(ele.getRight())

    # 각 걸음걸이 데이터값을 가져오기 위해서 데이터 값이 저장되어있는 class를 선언
    #각 12개 센서에 대해 각 걸음걸이데이터와 피어슨 상관관계분석 진행
    for i in range(12):
        nor_l = pd.DataFrame({"normal_l":normal_left[i], "ori_l":left[i]})
        corr = nor_l.corr(method='pearson')

        # 상관관계분석 진행
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0
        nor_mean.append(corr.values[0][1])
        # 상관관계분석값 중에서 쓰이는 수만 추출?해서 각 걸음걸이와의 상관계수 배열에 넣기
        nor_r = pd.DataFrame({"normal_r": normal_right[i], "ori_r": right[i]})
        corr = nor_r.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        nor_mean.append(corr.values[0][1])

        out_l = pd.DataFrame({"out_l": out_left[i], "ori_l": left[i]})
        corr = out_l.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        out_mean.append(corr.values[0][1])
        out_r = pd.DataFrame({"out_r": out_right[i], "ori_r": right[i]})
        corr = out_r.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        out_mean.append(corr.values[0][1])

        in_l = pd.DataFrame({"in_l": in_left[i], "ori_l": left[i]})
        corr = in_l.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        in_mean.append(corr.values[0][1])
        in_r = pd.DataFrame({"in_r": in_right[i], "ori_r": right[i]})
        corr = in_r.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        in_mean.append(corr.values[0][1])

        crane_l = pd.DataFrame({"crane_l": crane_left[i], "ori_l": left[i]})
        corr = crane_l.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        crane_mean.append(corr.values[0][1])
        crane_r = pd.DataFrame({"crane_r": crane_right[i], "ori_r": right[i]})
        corr = crane_r.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        crane_mean.append(corr.values[0][1])

        ele_l = pd.DataFrame({"ele_l": ele_left[i], "ori_l": left[i]})
        corr = ele_l.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        ele_mean.append(corr.values[0][1])
        ele_r = pd.DataFrame({"ele_r": ele_right[i], "ori_r": right[i]})
        corr = ele_r.corr(method='pearson')
        if math.isnan(corr.values[0][1]):
            corr.values[0][1] = 0;
        ele_mean.append(corr.values[0][1])
    dic = {0:avgList(nor_mean), 1:avgList(out_mean), 2:avgList(in_mean), 3:avgList(crane_mean), 4:avgList(ele_mean)}
    # 어떤 걸음걸이가 제일 상관있는지를 보기 위해서 dictionary로 선언

    dic_reverse = sorted(dic.items(), reverse=True, key=lambda item:item[1])
    if math.isnan(dic_reverse[0][1]):
        return 0, -1, -1
    #상관계수에 대해 내림차순 정렬

    percent = (int)((dic[0]+1)*50); #올바른 걸음걸이 척도 계산을 위한 상관계수(-1.0~+1.0)를 percentage(0~100)로 변경
    if dic_reverse[0][1] < 0.3:
        return 0, -1, -1
    # 각 걸음걸이 comment 및 질병예측 commnet를 가져오기 위한 class선언
    return percent, dic_reverse[0][0], dic_reverse[0][1]
    #올바른 걸음걸이 척도, 걸음걸이 comment, 질병 아이콘을 위해서(0~4)값 반환
    #{0:"정상걸음", 1:"팔자걸음", 2:"안짱걸음", 3:"학다리 걸음", 4:"11자 걸음"}


def COPAnalysis(leftPressure, rightPressure):
    left = copy.deepcopy(leftPressure)
    right = copy.deepcopy(rightPressure)
    left_point={0:[6.9, 5.3], 1:[6.2, 2.6], 2:[5.0, 5.6], 3:[3.1, 6.0], 4:[1.4, 7.0], 5:[1.6, 11.4], 6:[3.4, 12.8], 7:[2.0, 14.6], 8:[2.6, 21.1], 9:[3.8, 19.2], 10:[4.9, 20.9], 11:[4.0, 22.3]}
    right_point = {0:[1.2, 5.3], 1:[1.9, 2.6], 2:[3.1, 5.6], 3:[5.0, 6.0], 4:[6.7, 7.0], 5:[6.3, 11.4], 6:[4.5, 12.8], 7:[5.9, 14.6], 8:[5.3, 21.1], 9:[4.4, 19.2], 10:[3.0,20.9], 11:[4.1, 22.3]}

    # 형태를 변화시켜주기 위해 복사해서 사용
    left = np.asarray(left).reshape(10, -1)
    left = left.T
    left = left.tolist()
    right = np.asarray(right).reshape(10, -1)
    right = right.T
    right = right.tolist()
    left_max_index = []
    right_max_index = []
    for i in left:
        left_max_index.append(i.index(max(i)))
    for i in right:
        right_max_index.append(i.index(max(i)))

    for key, value in left_point.items():
        value[1] = 23.7 - value[1]
        value[1] = round(value[1], 2)

    for key, value in right_point.items():
        value[1] = 23.7 - value[1]
        value[1] = round(value[1], 2)

    sum = 0
    similarity = {}
    normal=normalGait()
    out_toe=out_toedGait()
    in_toe=in_toedGait()
    crane=craneGait()
    ele=elevenGait()

    G_normal_l, G_normal_r = normal.getGraph()
    G_out_l, G_out_r = out_toe.getGraph()
    G_in_l, G_in_r = in_toe.getGraph()
    G_crane_l, G_crane_r = crane.getGraph()
    G_ele_l, G_ele_r = ele.getGraph()

    G_user_l = nx.DiGraph()
    G_user_r = nx.DiGraph()
    G_user_l.add_nodes_from(left_max_index)
    G_user_r.add_nodes_from(right_max_index)
    pos_l = {}
    pos_r = {}
    for index in range(9):
        G_user_l.add_edge(left_max_index[index], left_max_index[index+1],length = calculateDistance(left_point[left_max_index[index]][0], left_point[left_max_index[index]][1], left_point[left_max_index[index+1]][0], left_point[left_max_index[index+1]][1]))
        G_user_r.add_edge(right_max_index[index], right_max_index[index+1],length = calculateDistance(right_point[right_max_index[index]][0], right_point[right_max_index[index]][1], right_point[right_max_index[index+1]][0], right_point[right_max_index[index+1]][1]))
        pos_l[index] = left_point[left_max_index[index]]
        pos_r[index] = right_point[right_max_index[index]]
    pos_l[9] = left_point[left_max_index[9]]
    pos_r[9] = right_point[right_max_index[9]]

    sum = nx.similarity.graph_edit_distance(G_normal_l, G_user_l)
    sum += nx.similarity.graph_edit_distance(G_normal_r, G_user_r)
    similarity[0] = (sum/2.0)
    sum = 0

    sum = nx.similarity.graph_edit_distance(G_out_l, G_user_l)
    sum += nx.similarity.graph_edit_distance(G_out_r, G_user_r)
    similarity[1] = (sum/2.0)
    sum = 0

    sum = nx.similarity.graph_edit_distance(G_in_l, G_user_l)
    sum += nx.similarity.graph_edit_distance(G_in_r, G_user_r)
    similarity[2] = (sum/2.0)
    sum = 0
    sum = nx.similarity.graph_edit_distance(G_crane_l, G_user_l)
    sum += nx.similarity.graph_edit_distance(G_crane_r, G_user_r)
    similarity[3] = (sum/2.0)
    sum = 0
    sum = nx.similarity.graph_edit_distance(G_ele_l, G_user_l)
    sum += nx.similarity.graph_edit_distance(G_ele_r, G_user_r)
    similarity[4] = (sum/2.0)
    sum = 0
    dic_reverse = sorted(similarity.items(), reverse=False, key=lambda item: item[1])
    return dic_reverse[0][0], dic_reverse[0][1]


def walkCheck(leftPressure, rightPressure):
    if len(leftPressure) != 120 or len(rightPressure) != 120:
        return 0, "결과가 바르지 못해 분석에 실패하였습니다.", -1
    elif math.isnan(leftPressure[0]) or math.isnan(rightPressure[0]):
        return 0, "조금만 더천천히 걸어주세요!", -1
    percent, disease_relative, relative = CheckEachSensorChange(leftPressure, rightPressure)

    disease_cop, similarity = COPAnalysis(leftPressure, rightPressure)

    comment = diseasePrediction()
    if disease_cop == disease_relative :
        return percent, comment.getComment(disease_cop), disease_cop
    elif similarity > 5:
        if disease_relative !=-1:
            return percent, comment.getComment(disease_relative), disease_relative
        elif similarity > 10:
            return 0, "현재 가지고 있는 걸음걸이 DB로는 파악이 불가한 걸음걸이입니다.", -1
        else :
            return 40, comment.getComment(disease_cop), disease_cop
    else :
        return 80, comment.getComment(disease_cop), disease_cop

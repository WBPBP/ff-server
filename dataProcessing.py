import sys;
import json
import numpy as np
import pandas as pd;
import copy
import random
from walkData import normalGait, out_toedGait, in_toedGait, craneGait, elevenGait, diseasePrediction
# walkData.py 파일에 기준이 되는 데이터들이나 comment를 적어놓았어요!

def balanceCheck(static_pressure_sum):
    # 정적족저압 검사의 결과로 서 있을 때 압력 합을 비교해서 무게중심이 어느쪽으로 치우쳐져있는지, 척추측만증이 의심되는지 판단하는 함수
    ary = np.array(static_pressure_sum);
    res = ary[0] - ary[1]; # 압력의 차이 계산(왼쪽 압력합(센서12개) 배열 - 오른쪽 압력합(센서12개) 배열)
    res1 = res.mean() # 압력 차이 평균을 내서 보통 압력의 차이가 어느정도인지 계산
    standard=15; # 척추측만증 판단 임시기준, 실험 후 변경 예정
    cnt=sum(abs(i)>standard for i in res); # 압력의 차이가 기준보다 높은 경우가 얼마나 나오는지 count, 여기 변경했어요!!!!
    comment=""
    if res1 > 2: # '왼-오'로 계산을 했기 때문에 압력 차의 평균 값이 양수인 경우 왼쪽으로 치우쳐져 있음
        comment = "몸의 무게중심이 왼쪽으로 치우쳐져 있는 경향이 보입니다."
    elif res1 < -2: # 압력 차의 평균이 음수인 경우 오른쪽으로 치우쳐져 있음
        comment = "몸의 무게중심이 오른쪽으로 치우쳐져 있는 경향이 보입니다."
    else: # 압력 차의 평균이=0인 경우 무게중심이 잘 잡혀있음
        comment = "몸무게가 양발에 고르게 분포해있어 몸의 균형은 안정적으로 보입니다."
    if (cnt > len(res) // 2) and (abs(res1)>2): #압력 차이가 기준보다 높은 것들의 수가 전체 개수의 반 이상이면 척추측만증 의심
        comment = comment + " 또한 현재 양쪽 발에 실리는 힘의 차이가 많은 것으로 보아 척추측만증을 의심해볼 수 있습니다."
    return comment # 몸의 무게중심이 어느쪽으로 치우쳐져 있는지, 척추측만증이 의심되는지에 대한 comment (문자열 형식입니다)

def avgList(list): # 형식이 list인 경우 전체 원소에 대한 평균을 구하는 함수
    return sum(list, 0.0)/len(list)

def pressureGraph(footstep_pressure_sum):
    # 걷는 동안의 왼, 오의 압력 합(센서12개)변화 그래프를 그리기 위한 값 형식 만들기
    left_mean=[]
    right_mean=[]
    index=0;
    for i in range(0, len(footstep_pressure_sum[0])-600, 600):
        #print(footstep_pressure_sum[1][i:i+600])
        left_mean.append(avgList(footstep_pressure_sum[0][i:i+600]))
        right_mean.append(avgList(footstep_pressure_sum[1][i:i+600]))
        index=i+600;
    left_mean.append(avgList(footstep_pressure_sum[0][index:]))
    right_mean.append(avgList(footstep_pressure_sum[1][index:]))
    last=len(footstep_pressure_sum[0][index:])
    left = np.arange(0, (len(left_mean)-1) * 30-29, 30);
    right = np.arange(0, (len(right_mean)-1) * 30-29, 30);
    left=left.tolist()
    left.append(left[len(left)-1]+(last/600)*30)
    right=right.tolist()
    right.append(right[len(right)-1]+(last/600)*30)
    left_mean.insert(0, 0)
    left_sum=[left, left_mean]
    # 왼발의 압력 합(센서12개)변화 그래프를 그리기 위한 [x축 값, y축 값]
    right_mean.insert(0, 0)
    right_sum=[right, right_mean]
    # 오른발의 압력 합(센서12개)변화 그래프를 그리기 위한 [x축 값, y축 값]
    return left_sum, right_sum

def walkCheck(footstep_pressure): # 걸음걸이 습관 파악 및 질병예측을 위한 함수
    left=copy.deepcopy(footstep_pressure[0])
    right=copy.deepcopy(footstep_pressure[1])
    # 형태를 변화시켜주기 위해 복사해서 사용
    left=np.asarray(left).reshape(12,-1)
    right=np.asarray(right).reshape(12,-1)
    # 해당 값이 아마도 list로 들어올 것같아서 일단 numpy배열 형식으로 변경하였습니다.
    # 또한 원래 12개 센서값들을 10개씩 가지고 있었어서배열의 형태도 [[센서1의 변화값(10)],[센서2의 변화값(10)],[센서3의 변화값(10)],.....] 변경
    nor_mean=[]
    out_mean=[]
    in_mean=[]
    crane_mean=[]
    ele_mean=[]
    # 상관분석 값들을 저장 list를 선언했습니다.

    normal=normalGait()
    out_toe=out_toedGait()
    in_toe=in_toedGait()
    crane=craneGait()
    ele=elevenGait()
    # 각 걸음걸이 데이터값을 가져오기 위해서 데이터 값이 저장되어있는 class를 선언

    #각 12개 센서에 대해 각 걸음걸이데이터와 피어슨 상관관계분석 진행
    for i in range(12):
        nor_l=pd.DataFrame({"normal_l":normal.getLeft()[i], "ori_l":left[i]})
        corr=nor_l.corr(method='pearson')
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
    dic_reverse=sorted(dic.items(), reverse=True, key=lambda item:item[1])
    #상관계수에 대해 내림차순 정렬

    percent=(int)((dic[0]+1)*50); #올바른 걸음걸이 척도 계산을 위한 상관계수(-1.0~+1.0)를 percentage(0~100)로 변경
    comment=diseasePrediction() # 각 걸음걸이 comment 및 질병예측 commnet를 가져오기 위한 class선언
    return percent, comment.getComment(dic_reverse[0][0]), dic_reverse[0][0]; #올바른 걸음걸이 척도, 걸음걸이 comment, 질병 아이콘을 위해서(0~4)값 반환
    #질병 아이콘은 한 걸음걸이(한 번호) 당 2~3개씩해서 안드로이드에서 번호에 맞는 아이콘을 출력하도록 할거에요
    #{0:"정상걸음", 1:"팔자걸음", 2:"안짱걸음", 3:"학다리 걸음", 4:"11자 걸음"}

def run(static_pressure_sum, footstep_pressure,step, footstep_pressure_sum): #전체 수행 함수(main이 안될 경우를 대비해 함수로 만들어 놓았어요!)
    static_comment = balanceCheck(static_pressure_sum);
    leftSum, rightSum = pressureGraph(footstep_pressure_sum)
    per, gait_comment, diseaseNum = walkCheck(footstep_pressure)

    dict = {"staticPressureRes": static_comment, "pressureGraphLeft": leftSum, "pressureGraphRight": rightSum,
            "step": step,
            "percent": per, "gaitComment": gait_comment, "diseaseNum": diseaseNum}
    '''
    staticPressureRes : 정적족저압 검사의 결과로 comment 입니다(string)
    pressureGraphLeft : 걷기 중의 왼발의 압력 합 변화를 위한 그래프를 그리기 위한 값입니다(int[x축][y축])
    pressureGraphRight : 걷기 중의 오른발의 압력 합 변화를 위한 그래프를 그리기 위한 값입니다(int[x축][y축])
    step : 걸음수입니다.(int)
    percent : 얼마나 올바르게 걸었는지 척도입니다.(int)
    gaitComment : 걸음걸이 및 질병 예측 comment입니다.(string)
    diseaseNum : 질병 아이콘 삽입을 위한 번호(int)
                {0:"정상걸음", 1:"팔자걸음", 2:"안짱걸음", 3:"학다리 걸음", 4:"11자 걸음"}
                0 : 아이콘 X, 1 : 허리디스크, 요통, 퇴행성 관절염 ,....
    '''

    print(json.dumps(dict, ensure_ascii=False))
    #return json.dumps(dict)


# 실제 사용시에 입력받을 부분입니다.

json_data=sys.argv[1]
print(sys.argv)

data=json.loads(json_data)
#print(data)
static_pressure_sum = data["key1"]
footstep_pressure = data["key2"]
step = data["key3"]
footstep_pressure_sum = data["key4"]
#print(static_pressure_sum)

static_pressure_sum=[[],[]]
footstep_pressure=[[],[]]
step=1300
footstep_pressure_sum=[[],[]]
for i in range(120):
    static_pressure_sum[0].append(random.randint(0, 200))
    static_pressure_sum[1].append(random.randint(0, 200))
    footstep_pressure[0].append(random.randint(0, 16))
    footstep_pressure[1].append(random.randint(0, 16))
for i in range(3400):
    footstep_pressure_sum[0].append(random.randint(0, 200))
    footstep_pressure_sum[1].append(random.randint(0, 200))
run(static_pressure_sum, footstep_pressure,step,footstep_pressure_sum)



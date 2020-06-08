
def isNumber(s) : 
    try:
	    float(s)
	    return True;
    except ValueError:
	    return False

# 정적족저압의 결과를 분석하여 comment를 반환해주는 함수입니다.
def analysisStaticPressureResult(verticalWeightBias_Left, verticalWeightBias_Right, horizontalWeightBias, heelPressureDifference):
    if not isNumber(verticalWeightBias_Left) or not isNumber(verticalWeightBias_Right) or not isNumber(horizontalWeightBias) or not isNumber(heelPressureDifference):
        return "검사 결과 분석이 불가능합니다."
    if verticalWeightBias_Left==-1 :
        coment = ""
    else:
        comment, leftState = verticalBalanceCheck_Left(verticalWeightBias_Left)

    if verticalWeightBias_Right != -1 :
        comment += verticalBalanceCheck_Right(verticalWeightBias_Right, leftState)
    if horizontalWeightBias != -1:
        comment += horizontalBalanceCheck(horizontalWeightBias)
    comment += scoliosisDiagnosis(heelPressureDifference)
    return comment

# 왼발의 앞/뒤꿈치의 균형 판단
def verticalBalanceCheck_Left(verticalWeightBias_Left):
    comment = "양 발 중 왼발은 "
    if verticalWeightBias_Left < 0.49:
        comment += "무게중심이 앞꿈치보다 뒤꿈치로 쏠려있는 경향이 보입니다."
        leftState = 0
    elif verticalWeightBias_Left > 0.51:
        comment += "무게중심이 뒤꿈치보다 앞꿈치로 쏠려있는 경향이 보입니다."
        leftState = 1
    else:
        comment += "무게가 왼발에 앞/뒤꿈치에 고르게 분포해있어 안정적으로 보입니다."
        leftState = 2
    return comment, leftState

# 오른발의 앞/뒤꿈치의 균형 판단
def verticalBalanceCheck_Right(verticalWeightBias_Right, leftState):
    if verticalWeightBias_Right < 0.49:
        comment = " 오른발 또한 " if(leftState==0) else " 하지만 오른발은"
        comment += "무게중심이 앞꿈치보다 뒤꿈치로 쏠려있는 경향이 보입니다."
    elif verticalWeightBias_Right > 0.51:
        comment = " 오른발 또한 " if (leftState == 1) else " 하지만 오른발은"
        comment += "무게중심이 뒤꿈치보다 앞꿈치로 쏠려있는 경향이 보입니다."
    else:
        comment = " 오른발 또한 " if (leftState == 2) else " 하지만 오른발은"
        comment += "무게가 왼발에 앞/뒤꿈치에 고르게 분포해있어 안정적으로 보입니다."
    return comment

# 양 발의 무게중심이 어느 쪽으로 치우쳐져 았는 판단
def horizontalBalanceCheck(horizontalWeightBias):
    comment = ""
    if horizontalWeightBias < 0.49:  # '왼-오'로 계산을 했기 때문에 압력 차값이 0에 가까울수록 몸의 무게중심이 왼발에 치우쳐져 있음
        comment = " \n몸의 무게중심은 왼쪽으로 치우쳐져 있는 경향이 보입니다."
    elif horizontalWeightBias > 0.51:  # 압력 차 편향이 1에 가까울수록 몸의 무게중심이 오른발에 치우쳐져 있음
        comment = " \n몸의 무게중심은 오른쪽으로 치우쳐져 있는 경향이 보입니다."
    else:  # 압력 차 편향이 0.5에 가까울수록 무게중심이 잘 잡혀있음
        comment = " \n몸 전체의 무게중심은 몸무게가 양발에 고르게 분포해있어 몸의 균형은 안정적으로 보입니다."
    return comment  # 몸의 무게중심이 어느쪽으로 치우쳐져 있는지 comment

# 척추측만증을 의심해볼 수 있는지 판단
def scoliosisDiagnosis(heelPressureDifference):
    comment = ""
    if heelPressureDifference > 29: #압력 차이가 기준보다 높은 것들의 수가 전체 개수의 반 이상이면 척추측만증 의심
        comment = " 또한 현재 양쪽 발에 실리는 힘의 차이가 크게 나는 것으로 보아 척추측만증을 의심해볼 수 있습니다."
    return comment

import random
import numpy as np

# 각 데이터들을 저장해놓은 파일입니다. 현재는 데이터가 없어서 생성자에 랜덤으로 설정해 놓은 것입니다.

class normalGait:
    __left=[];
    __right=[];
    def __init__(self):
        for i in range(120):
            self.__left.append(random.randint(0, 16))
            self.__right.append(random.randint(0, 16))
    def getLeft(self):
        return np.array(self.__left).reshape(12, -1)
    def getRight(self):
        return np.array(self.__right).reshape(12, -1)

class out_toedGait:
    __left=[];
    __right=[];

    def __init__(self):
        for i in range(120):
            self.__left.append(random.randint(0, 16))
            self.__right.append(random.randint(0, 16))

    def getLeft(self):
        return np.array(self.__left).reshape(12, -1)
    def getRight(self):
        return np.array(self.__right).reshape(12, -1)

class in_toedGait:
    __left=[];
    __right=[];

    def __init__(self):
        for i in range(120):
            self.__left.append(random.randint(0, 16))
            self.__right.append(random.randint(0, 16))

    def getLeft(self):
        return np.array(self.__left).reshape(12, -1)
    def getRight(self):
        return np.array(self.__right).reshape(12, -1)
class craneGait:
    __left=[];
    __right=[];

    def __init__(self):
        for i in range(120):
            self.__left.append(random.randint(0, 16))
            self.__right.append(random.randint(0, 16))

    def getLeft(self):
        return np.array(self.__left).reshape(12, -1)
    def getRight(self):
        return np.array(self.__right).reshape(12, -1)

class elevenGait:
    __left = [];
    __right = [];

    def __init__(self):
        for i in range(120):
            self.__left.append(random.randint(0, 16))
            self.__right.append(random.randint(0, 16))

    def getLeft(self):
        return np.array(self.__left).reshape(12, -1)
    def getRight(self):
        return np.array(self.__right).reshape(12, -1)

class diseasePrediction:
    __comment=["평균적으로 올바르게 걷는 습관을 가지고 있습니다.",
               "평균적으로 팔자걸음에 가까운 걸음걸이 습관을 가지고 있습니다. \n해당 걸음걸이를 계속 유지하실 경우 허리를 자꾸 뒤로 젖히게 되어 체중이 바깥쪽으로 쏠리면서 요통, 허리디스크, 퇴행성 관절염을 유발할 수 있습니다.",
               "평균적으로 안짱걸음에 가까운 걸음걸이 습관을 가지고 있습니다. \n해당 걸음걸이를 계속 유지하시는 경우 고관절염이 생길 수 있고 무릎인대가 손상될 수 있습니다.",
               "평균적으로 학다리걸음에 가까운 걸음걸이 습관을 가지고 있습니다. \n해당 걸음걸이를 계속 유지하시는 경우 무릎을 굽히지 않아 계속적으로 무릎에 충격이 가며 연골 연화증이 발생할 수 있습니다.",
               "평균적으로 일자걸음에 가까운 걸음걸이 습관을 가지고 있습니다. \n해당 걸음걸이를 계속 유지하시는 경우 무릎 안쪽에 체중이 부하되어 내측 관절에 염증이 생기거나 변형이 유발될 수 있습니다."];
    def getComment(self, index):
        return self.__comment[index]

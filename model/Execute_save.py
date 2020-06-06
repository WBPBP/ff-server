import json
import sys
import random


json_data=sys.argv[1]
data=json.loads(json_data)
verticalWeightBias_Left = data['verticalWeightBias_Left']
verticalWeightBias_Right = data['verticalWeightBias_Right']
horizontalWeightBias = data['horizontalWeightBias']
heelPressureDifference = data['heelPressureDifference']
leftPressure = data['leftPressure']
rightPressure = data['rightPressure']


f = open("./GaitData.txt", 'a')
f. write("left : " + str(leftPressure) + "\n")
f. write("right : " + str(rightPressure) + "\n\n")
f.close()
import os
import random
import json
random.seed(1)

NUMBER_OF_CARS = 5000

def generateRandomNo():
    return random.uniform(0,1)

historyObjs = {}
for carNo in range(NUMBER_OF_CARS):
    a = {
        'balanced': generateRandomNo(),
        'max_speed': generateRandomNo(),
        'min_length': generateRandomNo()
    }
    historyObjs['car-' + str(carNo)] = a

with open('app/entity/CarHistory.json', 'w') as f:
    json.dump(historyObjs, f)

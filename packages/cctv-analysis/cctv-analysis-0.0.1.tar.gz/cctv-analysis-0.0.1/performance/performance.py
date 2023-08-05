import os
import sys
sys.path.insert(0, '..')
from model.keras.yolo import YOLO
from model.openCv.OpenCv import OpenCV
from timeit import default_timer as timer
import numpy as np
import json


def load(model_name):
    if model_name.startswith("keras"):
        return YOLO()
    elif model_name.startswith("opencv"):
        version = model_name.split('_',1)[1]
        return OpenCV(version)
    else:
        raise ValueError(f"Model {model_name} not found")

#json resultados
performance = {}
data = []
videopath = 'people3.mp4'

def ejecutarModelo(modelName,videopath):
    model = load(modelName)
    print("empezo ejecucion de modelo")
    start = timer()
    resultado = model.analyze_video(videopath) #path de video
    end = timer()
    meanPersons = np.mean(resultado)
    tiempoTotal = end - start
    FPS_Promedio = ((len(resultado))/(end-start))
    dataJson = {
        'Modelo': modelName,
        'PersonasPromedio': meanPersons,
        'tiempoTotal': tiempoTotal,
        'FPS_Promedio': FPS_Promedio
    }
    data.append(dataJson)
    return dataJson

#OpenCV tiny
modelData = ejecutarModelo('opencv_tiny',videopath)
print(modelData)

#OpenCV 320
modelData = ejecutarModelo('opencv_320',videopath)
print(modelData)

#OpenCV 416
modelData = ejecutarModelo('opencv_416',videopath)
print(modelData)

#OpenCV 608
modelData = ejecutarModelo('opencv_608',videopath)
print(modelData)

#Keras
modelData = ejecutarModelo('keras_default',videopath)
print(modelData)


performance['DatosVideo'] = data
with open('{}.json'.format(videopath), 'w') as file:
    json.dump(performance, file, indent=4)
print(performance)





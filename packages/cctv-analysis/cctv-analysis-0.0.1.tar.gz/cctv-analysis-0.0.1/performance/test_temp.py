import os
import pathlib
import sys
#os.path.insert(0, '../model')
#from base import BaseModel
sys.path.insert(0, '../model/keras')
from yolo import YOLO
from timeit import default_timer as timer
import numpy as np
#archivo para pruebas

#os.system(f'python ../model/keras/yolo.py people3.mp4')
#os.system(f'python ../model/openCv/OpenCv.py people3.mp4 yolov3-320.cfg yolov3.weights')

kerasModel = load("yolo3")
print("empezo ejecucion de modelo")
start = timer()
resultado = kerasModel.analyze_video('people3.mp4')
end = timer()
meanPersons = np.mean(resultado)
print('Rendimiento ----------')
print('Personas encontradas en promedio por frame : ',meanPersons) 
print("tiempo total : ",end-start)
print("FPS promedio : ",((len(resultado))/(end-start)))
print('-----------------------')


'''funcion para imprimir json (se llama con -json_write(data))
        def json_write(data):
            #guardo datos en un archivo json
            with open('{}.json'.format(video_path), 'w') as file:
                json.dump(data, file, indent=4)

        def json_write(data):
            """guardo datos en un archivo json"""
            with open('data.json', 'w') as file:
                json.dump(data, file, indent=4)'''
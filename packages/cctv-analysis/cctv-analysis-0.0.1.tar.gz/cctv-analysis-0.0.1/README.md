# CCTV analysis.

A cctv analysis server to asynchronously analyse videos for objects such as persons or cars in cctv camera feeds.
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](LICENSE)

## Introduction.

KERAS implementation of YOLOv3 (Tensorflow backend) inspired by [allanzelener/YAD2K](https://github.com/allanzelener/YAD2K).

---

## Initial setup for model.

1. Clone the repository on your computer.
2. Download YOLOV3 weights and the yolo.h5 file from this drive link https://drive.google.com/drive/folders/1PHLAmDVdO3DWp0Igf2_T_uBnDsvJZghy?usp=sharing , or use de wget instruction above
3. Put the weights files in the weights folder "/cctv_analysis/model/weights", and the file yolo.h5 inside the cfg folder "/cctv_analysis/model/cfg".
4. Run the app.


To run the server localy:

At the server folder "cctv_analysis/server/"
python app.py  
server runs at http://127.0.0.1:5000/ localy,
use the "seleccionar archivo" button, then select video, once the video is selected click at the "enviar" button, after procesing the output can be found at the files folder (cctv_analysis/server/files" as a json file called data.

PD: the files folder can be modified from the user_cfg.json file at the server folder



# -*- coding: utf-8 -*-

import sys
import os
import json
import numpy as np
import tensorflow.compat.v1.keras.backend as K
import tensorflow as tf
tf.compat.v1.disable_eager_execution()
from timeit import default_timer as timer
from keras.models import load_model
from keras.layers import Input
#from keras.utils import multi_gpu_model
from PIL import Image, ImageFont, ImageDraw
#print(sys.path)
#sys.path.insert(0, './yolo3')
#print("syspath modificado",sys.path)
from ..base import BaseModel 
from model.keras.yolo3.utils import letterbox_image
from model.keras.yolo3.model import yolo_eval, yolo_body, tiny_yolo_body
import os


relative_path = os.path.dirname(os.path.relpath(__file__))


class YOLO(BaseModel):
    _defaults = {
        "model_path": '/../cfg/yolo.h5',
        "anchors_path": '/../cfg/yolo_anchors.txt',
        "classes_path": '/../cfg/coco_classes.txt',
        "score" : 0.3,
        "iou" : 0.45,
        "model_image_size" : (416, 416),
        "gpu_num" : 1,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"

    def __init__(self):
        self.__dict__.update(self._defaults) # set up default values
        self.class_names = self._get_class()
        self.anchors = self._get_anchors()
        self.sess = K.get_session()
        self.boxes, self.scores, self.classes = self.generate()


    def _get_class(self):
        classes_path = relative_path+str(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def _get_anchors(self):
        anchors_path = relative_path+str(self.anchors_path)
        with open(anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def generate(self):
        model_path = relative_path+str(self.model_path)
        assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

        # Load model, or construct model and load weights.
        num_anchors = len(self.anchors)
        num_classes = len(self.class_names)
        is_tiny_version = num_anchors==6 # default setting
        try:
            self.yolo_model = load_model(model_path, compile=False)
        except:
            self.yolo_model = tiny_yolo_body(Input(shape=(None,None,3)), num_anchors//2, num_classes) \
                if is_tiny_version else yolo_body(Input(shape=(None,None,3)), num_anchors//3, num_classes)
            self.yolo_model.load_weights(self.model_path) # make sure model, anchors and classes match
        else:
            assert self.yolo_model.layers[-1].output_shape[-1] == \
                num_anchors/len(self.yolo_model.output) * (num_classes + 5), \
                'Mismatch between model and given anchor and class sizes'

        print('{} model, anchors, and classes loaded.'.format(model_path))
        
        # Generate output tensor targets for filtered bounding boxes.
        # Lo guardamos por las dudas (conf GPU)
        self.input_image_shape = K.placeholder(shape=(2, ))
        '''if self.gpu_num>=2:
            self.yolo_model = multi_gpu_model(self.yolo_model, gpus=self.gpu_num)'''
        boxes, scores, classes = yolo_eval(self.yolo_model.output, self.anchors,
                len(self.class_names), self.input_image_shape,
                score_threshold=self.score, iou_threshold=self.iou)
        return boxes, scores, classes
    
    def analyze_frame(self, image):
        if self.model_image_size != (None, None):
            assert self.model_image_size[0]%32 == 0, 'Multiples of 32 required'
            assert self.model_image_size[1]%32 == 0, 'Multiples of 32 required'
            boxed_image = letterbox_image(image, tuple(reversed(self.model_image_size)))
        else:
            new_image_size = (image.width - (image.width % 32),
                              image.height - (image.height % 32))
            boxed_image = letterbox_image(image, new_image_size)
        image_data = np.array(boxed_image, dtype='float32')
        image_data /= 255.
        image_data = np.expand_dims(image_data, 0)  # Add batch dimension.
        '''filtrar cajas con puntajes mayores a 0.3'''

        out_boxes, out_scores, out_classes = self.sess.run(
            [self.boxes, self.scores, self.classes],
            feed_dict={
                self.yolo_model.input: image_data,
                self.input_image_shape: [image.size[1], image.size[0]],
                K.learning_phase(): 0
            })
        cantNoPersona = 0
        for objeto in out_classes:
            if objeto != 0:
                cantNoPersona = cantNoPersona + 1
        #data['list'].append((len(out_boxes)-cantNoPersona))
        return (len(out_boxes)-cantNoPersona)


    def close_session(self):
        self.sess.close()

    def analyze_video(self, video_path):
        import cv2
        vid = cv2.VideoCapture(video_path)
        if not vid.isOpened():
            raise IOError("Couldn't open webcam or video")
        video_FourCC     = cv2.VideoWriter_fourcc(*'XVID')
        video_fps       = vid.get(cv2.CAP_PROP_FPS)
        video_size      = (int(vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
                            int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        results = []
        while True:
            print(".")
            return_value, frame = vid.read()
            if not return_value:
                break
            image = Image.fromarray(frame)
            results.append(self.analyze_frame(image))
        return results


import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image

app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
img = ins_get_image('t1')
faces = app.get(img)
rimg = app.draw_on(img, faces)
cv2.imwrite("Richard_Stallman_at_LibrePlanet_2019.jpg", rimg)


# Method-1, use FaceAnalysis
# app = FaceAnalysis(allowed_modules=['detection']) # enable detection model only
# app.prepare(ctx_id=0, det_size=(640, 640))

# # Method-2, load model directly
# detector = insightface.model_zoo.get_model('your_detection_model.onnx')
# detector.prepare(ctx_id=0, input_size=(640, 640))
# handler = insightface.model_zoo.get_model('your_recognition_model.onnx')
# handler.prepare(ctx_id=0)

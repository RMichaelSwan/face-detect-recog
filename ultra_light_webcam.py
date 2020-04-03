#! /usr/bin/env python3
import cv2
import dlib
import numpy as np
from imutils import face_utils
from box_utils import *

import onnx
import onnxruntime as ort
from onnx_tf.backend import prepare
import time

video_capture = cv2.VideoCapture(0)
# video_capture.set(cv2.CAP_PROP_FPS, 5) # FPS setting does not work on all cameras

onnx_path = "./UltraLight/models/ultra_light_640.onnx"
onnx_model = onnx.load(onnx_path)
predictor = prepare(onnx_model)
ort_session = ort.InferenceSession(onnx_path)
input_name = ort_session.get_inputs()[0].name


hogFaceDetector = dlib.get_frontal_face_detector()


shape_predictor = dlib.shape_predictor(
    "FacialLandmarks/shape_predictor_5_face_landmarks.dat"
)
fa = face_utils.facealigner.FaceAligner(
    shape_predictor, desiredFaceWidth=112, desiredLeftEye=(0.3, 0.3)
)

frame_rate = 30
prev = 0

while True:
    ###manual framerate handling (for cameras that don't support slower FPS)
    time_elapsed = time.time() - prev
    ret, frame = video_capture.read()  # needed to clear camera buffer

    if time_elapsed > 1.0 / frame_rate:
        prev = time.time()
        ###end framerate handling
        if frame is not None:
            h, w, _ = frame.shape

            # preprocess img acquired
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # convert bgr to rgb

            def Ultralight_Detect():
                # extra ultralight required pre-processing
                img = cv2.resize(img, (640, 480))
                img_mean = np.array([127, 127, 127])
                img = (img - img_mean) / 128
                img = np.transpose(img, [2, 0, 1])
                img = np.expand_dims(img, axis=0)
                img = img.astype(np.float32)

                confidences, boxes = ort_session.run(None, {input_name: img})
                boxes, labels, probs = predict(w, h, confidences, boxes, 0.7)

                for i in range(boxes.shape[0]):
                    box = boxes[i, :]
                    x1, y1, x2, y2 = box
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    shape = shape_predictor(
                        gray, dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2)
                    )
                    shape = face_utils.shape_to_np(shape)
                    for (x, y) in shape:
                        cv2.circle(frame, (x, y), 2, (80, 18, 236), -1)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 18, 236), 2)
                    cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (80, 18, 236), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    text = f"Face: {round(probs[i], 2)}"
                    cv2.putText(
                        frame, text, (x1 + 6, y2 - 6), font, 0.3, (255, 255, 255), 1
                    )

            def Dlib_Detect():
                dets, probs, idx = hogFaceDetector.run(img, 0, 0)
                for i, d in enumerate(dets):
                    x1 = d.left()
                    y1 = d.top()
                    x2 = d.right()
                    y2 = d.bottom()

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    shape = shape_predictor(
                        gray, dlib.rectangle(left=x1, top=y1, right=x2, bottom=y2)
                    )
                    shape = face_utils.shape_to_np(shape)
                    for (x, y) in shape:
                        cv2.circle(frame, (x, y), 2, (80, 18, 236), -1)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (80, 18, 236), 2)
                    cv2.rectangle(
                        frame, (x1, y2 - 20), (x2, y2), (80, 18, 236), cv2.FILLED
                    )
                    font = cv2.FONT_HERSHEY_DUPLEX
                    text = f"Face: {round(probs[i], 2)}"
                    cv2.putText(
                        frame, text, (x1 + 6, y2 - 6), font, 0.3, (255, 255, 255), 1
                    )

            Dlib_Detect()
            cv2.imshow("Video", frame)

        # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

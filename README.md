# face-detect-recog

Some experiments with face detection and recognition

## Face Detection


### Compatibility

* All code written for Python 3
* Tested on Ubuntu 18.04 successfuly
* Mac OSX had dependency issues for running ultralight model (onnx library)
* Windows had dependency issues for running ultralight model (onnx library must be compiled in Windows)


### Run Instructions

1. Install requirements: `pip install -r requirements.txt`
1. Test it! `python detector_test.py`


### Notes

Hardware used: 8 cores, 9th generation Intel i7

Currently it seems that Dlib is doing the best in terms of efficiency, but it has questionable performance if upsampling is needed or if faces are in non-standard orientations (looking up, down, side). It's also unclear if Dlib is actually parallelized, though it uses so little processing power (7% on possibly 1 core?), this may not matter.

Ultralight face/eye detector with some pre-processing uses 20% CPU (on each core) at 5fps, ~40% at 10fps, 45-60% at 20fps

# TODO

Take in arguments for different framerates and detection algorithms <https://docs.python.org/3/library/argparse.html>
Finish recognition part of tutorial: <https://github.com/fyr91/face_detection> and <https://towardsdatascience.com/real-time-face-recognition-with-cpu-983d35cc3ec5>
Investigate other face recognition methods: <https://github.com/ageitgey/face_recognition>; <https://github.com/zma-c-137/VarGFaceNet>  

# References

Dlib code sources: <https://www.learnopencv.com/face-detection-opencv-dlib-and-deep-learning-c-python/> and <http://dlib.net/face_detector.py.html>

import time

import cv2 as cv
import skvideo.io


fourcc = cv.VideoWriter.fourcc(*'yuv2')
out = skvideo.io.FFmpegWriter('data/output.mp4', outputdict={
  '-vcodec': 'libx264', '-crf': '0', '-preset': 'fast', '-r': '60'})
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv.CAP_PROP_FPS, 60)

start = time.time()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    out.writeFrame(frame[:, :, ::-1])
    if time.time() - start > 3:
        break

cap.release()
out.close()

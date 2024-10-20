from stitching import Stitcher
import os
import cv2

os.environ['KMP_WARNINGS'] = '0'

def create_panorama(video):
  # Check if the video object is valid
  if not video.isOpened():
    print("Error: Could not open video.")
    exit()

  # Get video frame rate (fps)
  fps = video.get(cv2.CAP_PROP_FPS)

  # Extract 1/10th of the frames
  frame_number = 0
  extracted_frames = []

  while video.isOpened():
    ret, frame = video.read()
    
    if not ret:
      break  # Video is finished or cannot read frame

    # Add every 1/10th frame to the list
    if frame_number % 10 == 0:
      extracted_frames.append(frame)

    frame_number += 1

  # Release the video capture object
  video.release()

  print(f"read frames {len(extracted_frames)}")
  settings = {"detector": "sift", "confidence_threshold": 0.05, "matches_graph_dot_file": False, "crop": False}
  stitcher = Stitcher(**settings)

  print("stitching")
  panorama = stitcher.stitch(extracted_frames)

  cv2.imwrite("pano.png", panorama)
  
  return panorama

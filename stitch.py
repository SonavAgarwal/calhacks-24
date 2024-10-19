from stitching import Stitcher
import cv2
import os
os.environ['KMP_WARNINGS'] = '0'


print("importerd")
# Set up video file
video_path = 'test.mov'

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video frame rate (fps)
fps = cap.get(cv2.CAP_PROP_FPS)

# Extract 1/10th of the frames
# frame_interval = int(fps / 10)  # Capture one frame for every 0.1 seconds

frame_number = 0
extracted_frames = []

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        break  # Video is finished or cannot read frame

    # Add every 1/10th frame to the list
    if frame_number % 10 == 0:
        # resized_frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        extracted_frames.append(frame)

    frame_number += 1

# Release the video capture object
cap.release()
cv2.imshow("image",extracted_frames[0])

print(f"read frames {len(extracted_frames)}")
stitcher = Stitcher()
settings = {"detector": "sift", "confidence_threshold": 0.15,"matches_graph_dot_file":True,"crop":False}
stitcher = Stitcher(**settings)

print("stritiching")
panorama = stitcher.stitch(extracted_frames)

cv2.imshow("image",panorama)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()
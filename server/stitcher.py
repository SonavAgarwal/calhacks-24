from stitching import Stitcher
import os
import cv2

os.environ['KMP_WARNINGS'] = '0'

def create_panorama(path):
    # Set up video file
    video_path = path

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

    print(f"read frames {len(extracted_frames)}")
    stitcher = Stitcher()
    settings = {"detector": "sift", "confidence_threshold": 0.05,"matches_graph_dot_file":False,"crop":False}
    stitcher = Stitcher(**settings)

    print("stitching")
    panorama = stitcher.stitch(extracted_frames)

    cv2.imwrite("pano.png",panorama)
    
    return panorama

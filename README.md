# ZED_Hand_Tracking
Tracking 3D positions of hand landmarks using a ZED 2i Camera, OpenCV, and MediaPipe.
Make sure that you have already installed ZED SDK, OpenCV and MediaPipe.
## testing.ipynb
DON'T USE THIS FILE. (I use it for testing purposes.)
## run.ipynb
This file will 1. Open the ZED Camera or Open a Recorded .svo file, 2. Run the hand tracking using OpenCV and MediaPipe, 3. Visuallizing in OpenCV and Matplot.
1. Takes the streamed video from ZED camera or gets recorded (.svo) video
2. Processes the image
3. Outputs the image with hand landmarks overlayed
4. Outputs a 3D scatter plot visualizing the 3D postion of each hand landmark
## record_svo_file.ipynb
Run this file to record video (.svo), need to specify the filename in the .ipynb file.

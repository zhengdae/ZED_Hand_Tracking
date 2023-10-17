# ZED_Hand_Tracking
Tracking 3D positions of hand landmarks using a ZED 2i Camera, OpenCV, and MediaPipe.
Make sure that you have already installed ZED SDK, OpenCV and MediaPipe.
## testing.ipynb
DON'T USE THIS FILE. (I use it for testing purposes.)
## live_stream.ipynb
This file will 1. Open the ZED Camera, 2. Get the live stream video, 3. Run the hand tracking using OpenCV and MediaPipe, 4. Visuallizing in OpenCV and Matplot.
1. Takes the streamed video from ZED camera,
2. Processes the image
3. Outputs the image with hand landmarks overlayed
4. Outputs a 3D scatter plot visualizing the 3D postion of each hand landmark

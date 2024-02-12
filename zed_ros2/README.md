# Introduction:
To synchronize the data recording, we are going to use ROS2 to record the data: 
1. Left Image,
2. Right Image,
3. Point Cloud Data or Depth Image from ZED, 
4. Shimmer Sensors, 
5. Viper EM Trackers, etc.

I made several attempts, please see Option 1 and Option 2, hopefully not Option 3. 
    
# Option 1: 
1. Record left image, right image, and point cloud data from ZED Camera into a ROS2 Bag file, 
2. Extract images as .png files,
3. Extract point cloud data as .csv files,
4. Conduct hand tracking using MediaPipe. 

Problem:
1. Inconsistent timestamps or inconsistent sampling frequency, especially Point Cloud data
2. Point Cloud data is such a BIG file
    
# Option 2:
1. Record left image, right image, and depth image (not point cloud this time),
2. Use Python codes to record the images, NOT bag file, plus recording synchronization.
3. Extract images as .png files,
4. Conduct hand tracking using MediaPipe.

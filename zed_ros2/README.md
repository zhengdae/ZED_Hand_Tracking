# Introduction:
    To synchronize the data recording, we are going to use ROS2 to record the data: 
    1. Left Image,
    2. Right Image,
    3. Point Cloud Data or Depth Image from ZED, 
    4. Shimmer Sensors, 
    5. Viper EM Trackers, etc.

RESOLUTION: VGA (672 * 376), THE LOWESET RESOLUTION, RATE: 60 HZ

I made several attempts, please see Option 1, Option 2, Option 3, and Option 4 (last option). 

# Option 1: ROS2 BAG for RECORDING (not recommended)
    1. Record left image, right image, and point cloud data/depth image from ZED Camera into a ROS2 Bag file, 
    2. Extract images as .png files,
    3. Extract point cloud data as .csv files,
    4. Conduct hand tracking using MediaPipe. 

    Problem:
    1. Inconsistent timestamps or inconsistent sampling frequency, especially Point Cloud data,
    2. Point Cloud data is such a BIG file. 
    
# Option 2: PYTHON for RECORDING
    1. Record left image, right image, and point cloud data,
    2. Use Python codes to record the images and point cloud data in real time. NOT bag files, plus recording synchronization,
    3. Use OpenCV to save images as .png files,
    4. Use Numpy to save point cloud as .npy files, (Saving to .csv is very slow, bad for saving efficiency)
    5. Conduct hand tracking using MediaPipe. 

    Problem:
    1. Saving Point Cloud is slow and resulting in BIG files, still inconsistent frequency. 
    2. Extracting XYZ from PointCloud2 messages is tricky. (Working on this)

# Option 3: PYTHON for RECORDING (recommended)
    1. Record left image, right image, and depth image, 
    2. Use Python codes to record the images in real time. NOT bag files, plus recording synchronization,
    3. Use OpenCV to save left and right images as .png files, 
    4. Use Numpy to save depth image as .npy files. (Saving to .csv is very slow, bad for saving efficiency)
    5. Conduct hand tracking using MediaPipe. 

    Problem:
    1. Unlike PointCloud2 message, Depth message only have distance in Z direction, pixel info for X and Y directions.
    
# Option 4: PYTHON for RECORDING (HIGH RESOLUTION)
    Recording either point cloud or depth info from ROS topics is harmful to Resolution and Frame Rate. 
    To achieve a better resolution and a better frame rate.
    1. Only record left and right images,
    2. Use Python codes to record the images in real time. NOT bag files, plus recording synchronization,
    3. Use OpenCV to save left and right images as .png files,
    4. Conduct hand tracking using MediaPipe using both left and right images. 
    5. Calculate the landmark's 3D position by 3D reconstruction using cameras parameters (focal length, baseline, etc.)

    Problem:
    1. A lot of post processing efforts. 

import numpy as np
import pyzed.sl as sl

class ZED():
    def __init__(self, fps = None, depth_min_distance = 0.2, depth_max_distance = 3, input_filename = None):
        if input_filename is None:
            print("Using Live Stream from ZED")
            self.input_type = sl.InputType()
            self.svo_mode = False
        else:
            print(f"Reading SVO File: {0}".format(input_filename))
            self.input_type = sl.InputType()
            self.input_type.set_from_svo_file(input_filename)
            self.svo_mode = True
            
        self.camera = sl.Camera()
        self.init_params = sl.InitParameters(input_t = self.input_type)

        if fps is not None:
            self.init_params.camera_fps = fps
            
        self.init_params.coordinate_units = sl.UNIT.METER
        self.init_params.depth_minimum_distance = depth_min_distance
        self.init_params.depth_maximum_distance = depth_max_distance

        self.image = sl.Mat()
        self.depth = sl.Mat()
        self.point_cloud = sl.Mat()

    def enable_recording(self, output_filename):
        if output_filename is not None:
            recording_param = sl.RecordingParameters(output_filename, sl.SVO_COMPRESSION_MODE.H264)
            err = self.camera.enable_recording(recording_param)
            if err != sl.ERROR_CODE.SUCCESS:
                print("RECORDING ZED: ", err)
                

    def config_resolution(self, resolution = "HD720"):
        # Configure Resolution
        if resolution == "HD2K":
            self.init_params.camera_resolution = sl.RESOLUTION.HD2K
            if self.init_params.camera_fps not in [15]:
                print("HD2K requires a Frame Rate (fps) of 15")
        if resolution == "HD1080":
            self.init_params.camera_resolution = sl.RESOLUTION.HD1080
            if self.init_params.camera_fps not in [15, 30]:
                print("HD1080 requires a Frame Rate (fps) of 15 or 30")
        if resolution == "HD720":
            self.init_params.camera_resolution = sl.RESOLUTION.HD720
            if self.init_params.camera_fps not in [15, 30, 60]:
                print("HD720 requires a Frame Rate (fps) of 15, 30, 60")
        if resolution == "VGA":
            self.init_params.camera_resolution = sl.RESOLUTION.VGA
            if self.init_params.camera_fps not in [15, 30, 60, 100]:
                print("VGA requires a Frame Rate (fps) of 15, 30, 60, 100")
        
        
    def config_depth_mode(self, depth_mode = "NEURAL"):
        # Configure Depth Mode
        if depth_mode == "NEURAL":
            self.init_params.depth_mode = sl.DEPTH_MODE.NEURAL
        if depth_mode == "ULTRA":
            self.init_params.depth_mode = sl.DEPTH_MODE.ULTRA
        if depth_mode == "QUALITY":
            self.init_params.depth_mode = sl.DEPTH_MODE.QUALITY
        if depth_mode == "PERFORMANCE":
            self.init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE
        if depth_mode == "None":
            self.init_params.depth_mode = sl.DEPTH_MODE.NONE
        


    def open_camera(self, fill_mode = True):
        err = self.camera.open(self.init_params)
        if err != sl.ERROR_CODE.SUCCESS:
            print("Failed to Open ZED!")
        else:
            print("Open ZED Successfully!")
        # Set Runtime Parameters for Camera
        self.runtime_params = sl.RuntimeParameters()
        self.runtime_params.enable_fill_mode = fill_mode
    
    def get_calibration_params(self):
        self.camera_params = self.camera.get_camera_information().camera_configuration.calibration_parameters.left_cam
        self.fx = self.camera_params.fx
        self.fy = self.camera_params.fy
        self.cx = self.camera_params.cx
        self.cy = self.camera_params.cy

    def get_image(self):
        self.camera.retrieve_image(self.image, sl.VIEW.LEFT)
        # self.camera.retrieve_measure(self.depth, sl.MEASURE.DEPTH)
        self.camera.retrieve_measure(self.point_cloud, sl.MEASURE.XYZRGBA, sl.MEM.CPU)
        # convert to the format that MediaPipe can process
        self.image_cv2 = self.image.get_data()
        # self.depth_cv2 = self.depth.get_data()
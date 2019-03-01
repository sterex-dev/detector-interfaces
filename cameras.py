import os
import configparser

class camera(object):
    def __init__(self):
        self.camera = None

    def connect(self):
        pass

    def disconnect(self):
        pass

    def getAOI(self):
        pass

    def getBandwidthAssigned(self):
        pass

    def getBandwidthReserve(self):
        pass

    def getBinningHorizontal(self):
        pass

    def getBinningHorizontalMode(self):
        pass

    def getBinningVertical(self):
        pass

    def getBinningVerticalMode(self):
        pass

    def getBlackLevel(self):
        pass

    def getExposureTimeMicroseconds(self):
        pass

    def getFrameRate(self):
        pass
        
    def getGain(self):
        pass  

    def getGainAuto(self):
        pass     
                      
    def getImageFlipX(self):
        pass

    def getImageFlipY(self):
        pass

    def getIPD(self):        
        pass

    def getMaxNumBuffers(self):
        pass

    def getFrameOverheadsSeconds(self):
        pass

    def getPacketSize(self):
        pass

    def getPayloadSize(self):
        pass

    def getPixelFormat(self):
        pass

    def getReadoutTime(self):
        pass

    def getTemperature(self, sensor_name):
        pass

    def getTemperatureState(self, sensor_name):
        pass

    def getThroughputCurrent(self):
        pass
        
    def getTransmissionStartDelay(self):
        pass  

    def read(self, n_images, read_timeout_ms):
        pass

    def sendParameters(self, config):
        try:
            exptime = int(config['EXPTIME'])
        except KeyError:
            exptime = None  
        try:
            pixel_format = str(
                config['PIXEL_FORMAT'])
        except KeyError:
            pixel_format = None                  
        try:
            x_offset = int(config['IMAGE_X_OFFSET'])
        except KeyError:
            x_offset = None
        try:
            y_offset = int(config['IMAGE_Y_OFFSET'])
        except KeyError:
            y_offset = None				
        try:
            width = int(config['IMAGE_WIDTH'])
        except KeyError:
            width = None	
        try:
            height = int(config['IMAGE_HEIGHT'])
        except KeyError:
            height = None
        try:
            gain = int(config['GAIN'])
        except KeyError:
            gain = None
        try:
            gain_auto = str(
                config['GAIN_AUTO'])
        except KeyError:
            gain_auto = None           
        try:
            bias = int(config['BIAS'])
        except KeyError:
            bias = None
        try:
            binning_h = int(config['BINNING_H'])
        except KeyError:
            binning_h = None
        try: 
            binning_v = int(config['BINNING_V'])
        except KeyError:
            binning_v = None
        try:
            binning_mode = str(config['BINNING_MODE'])
        except KeyError:
            binning_mode = None
        try:
            frame_rate = int(config['FRAME_RATE'])
        except KeyError:
            frame_rate = None
        try:
            acquisition_mode = str(
                config['ACQUISITION_MODE'])
        except KeyError:
            acquisition_mode = None
        try:
            reverse_x = int(
                config['REVERSE_X'])
        except KeyError:
            reverse_x = None           
        try:
            reverse_y = int(
                config['REVERSE_Y'])
        except KeyError:
            reverse_y = None    

        if self.camera is not None:
            if exptime is not None:
                self.setExposureTimeMicroseconds(exptime)
            if pixel_format is not None:
                self.setPixelFormat(pixel_format)
            if width is not None and height is not None and \
            x_offset is not None and y_offset is not None:
                self.setAOI(width, height, x_offset, y_offset)
            if binning_h is not None:
                self.setBinningHorizontal(binning_h)
            if binning_v is not None:
                self.setBinningVertical(binning_v)
            if binning_mode is not None:
                self.setBinningHorizontalMode(binning_mode)
                self.setBinningVerticalMode(binning_mode)            
            if gain is not None:
                self.setGain(gain)
            if gain_auto is not None:
                self.setGainAuto(gain_auto)            
            if bias != None:
                self.setBlackLevel(bias)
            if frame_rate is not None:
                self.setFrameRate(frame_rate)
            if acquisition_mode is not None:
                self.setAcquisitionMode(acquisition_mode)
            if reverse_x is not None:
                if reverse_x == 1:
                    self.setImageFlipX(True)
                else:
                    self.setImageFlipX(False)
            if reverse_y is not None:
                if reverse_y == 1:
                    self.setImageFlipY(True)
                else:
                    self.setImageFlipY(False)

    def setAOI(self, w, h, x_offset, y_offset):
        pass

    def setAcquisitionMode(self, mode):
        pass

    def setBinningHorizontal(self, binning):
        pass
        
    def setBinningHorizontalMode(self, mode):
        pass

    def setBinningVertical(self, binning):
        pass

    def setBinningVerticalMode(self, mode):
        pass

    def setBlackLevel(self, level):
        pass

    def setExposureTimeMicroseconds(self, exposure_time):
        pass

    def setFrameRate(self, frame_rate):
        pass

    def setGain(self, gain):
        pass 

    def setGainAuto(self, gain_auto):
        pass    

    def setImageFlipX(self, flip):
        pass

    def setImageFlipY(self, flip):
        pass

    def setIPD(self, delay):
        pass

    def setMaxNumBuffers(self, max_num_buffers):
        pass

    def setPacketSize(self, size):
        pass

    def setPixelFormat(self, pixel_format):
        pass

    def setTransmissionStartDelay(self, delay):
        pass      

    def showLiveFeed(self):
        pass
    
    def showLiveFeed_callback_mousemove(self):
        pass

    def showLiveFeed_logic(self):
        pass

    def showLiveFeed_render(self):
        pass

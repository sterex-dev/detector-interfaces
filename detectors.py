class detector(object):
    '''
        Any new camera should implement the following functions.
    '''
    def __init__(self):
        pass
    def connect(self):
        pass
    def disconnect(self):
        pass
    def expose(self, max_number_of_exposures=0):
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
    def getThroughputCurrent(self):
        pass
    def getTransmissionStartDelay(self):
        pass  
    def readNImagesFromBuffer(self, n_images, read_timeout_S, 
        time_between_read_attempts_S):
        pass
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

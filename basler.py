import time

from pypylon import pylon
from pypylon import genicam

from detector import detector

class Basler_2040_35gm(detector):
    def __init__(self):
        self.exposure_start_delay_uS = 35

    def connect(self):
        self.camera = pylon.InstantCamera(
            pylon.TlFactory.GetInstance().CreateFirstDevice())

    def disconnect(self):
        pass

    def expose(self, max_number_of_exposures=0):
        if max_number_of_exposures == 0:
            self.camera.StartGrabbing() 
        else:
            self.camera.StartGrabbingMax(max_number_of_exposures)

    def getAOI(self, w, h, x_offset, y_offset):
        self.camera.Open()
        w = self.camera.Width.GetValue()
        h = self.camera.Height.GetValue()
        x_offset = self.camera.OffsetX.GetValue()
        y_offset = self.camera.OffsetY.GetValue()
        self.camera.Close()    
        return (w, h, x_offset, y_offset)

    def getBandwidthAssigned(self):
        '''
            Bandwidth assigned to camera in bytes/s, a function of network.
        '''
        self.camera.Open()
        bwa = self.camera.GevSCBWA.GetValue()
        self.camera.Close()
        return bwa

    def getBandwidthReserve(self):
        '''
            % of bwa reserved to resend packets.
        '''
        self.camera.Open()
        bwr = self.camera.GevSCBWRA.GetValue()
        self.camera.Close()
        return bwr
       
    def getBinningHorizontal(self):
        self.camera.Open()
        binning = self.camera.BinningHorizontal.GetValue()
        self.camera.Close()
        return binning

    def getBinningHorizontalMode(self):
        self.camera.Open()
        binning = self.camera.BinningHorizontalMode.GetValue()
        self.camera.Close()
        return binning        

    def getBinningVertical(self):
        self.camera.Open()
        binning = self.camera.BinningVertical.GetValue()
        self.camera.Close()
        return binning

    def getBinningVerticalMode(self):
        self.camera.Open()
        binning = self.camera.BinningVerticalMode.GetValue()
        self.camera.Close()
        return binning        

    def getBlackLevel(self):
        self.camera.Open()
        level = self.camera.BlackLevelRaw.GetValue()
        self.camera.Close()
        return level  

    def getExposureTimeMicroseconds(self):
        self.camera.Open()
        exposure_time = self.camera.ExposureTimeAbs.GetValue()
        self.camera.Close()
        return exposure_time

    def getFrameRate(self):
        self.camera.Open()
        frame_rate = self.camera.ResultingFrameRateAbs.GetValue()
        self.camera.Close()      
        return frame_rate 

    def getGain(self):
        self.camera.Open()
        gain = self.camera.GainRaw.GetValue()
        self.camera.Close()
        return gain

    def getGainAuto(self):
        self.camera.Open()
        gain = self.camera.GainAuto.GetValue()
        self.camera.Close()
        return gain                    

    def getImageFlipX(self):
        self.camera.Open()
        flip = self.camera.ReverseX.GetValue()
        self.camera.Close()      
        return flip

    def getImageFlipY(self):
        self.camera.Open()
        flip = self.camera.ReverseY.GetValue()
        self.camera.Close() 
        return flip    

    def getIPD(self):
        '''
            Get delay between sending packets in ticks.
        '''
        self.camera.Open()
        delay = self.camera.GevSCPD.GetValue()
        self.camera.Close() 
        return delay          

    def getMaxNumBuffers(self):
        self.camera.Open()
        max_num_buffers = self.camera.MaxNumBuffer.GetValue()
        self.camera.Close()
        return max_num_buffers  

    def getFrameOverheadsSeconds(self):
        '''
            Get overheads breakdown:
                - delay between triggering and start (exposure_start_delay),
                - time to readout (readout_time)
                - time between reading out and transmitting 
                (transmission_start_delay)
                - time to transfer frame to host (transmission_delay)
        '''
        transmission_delay_uS = self.getPayloadSize()/\
            self.getThroughputCurrent()*10**6
        transmission_start_delay_uS = self.getTransmissionStartDelay()       
        readout_time_uS = self.getReadoutTime()       
        overheads = {
            'exposure_start_delay': self.exposure_start_delay_uS/10**6,
            'readout_time': readout_time_uS/10**6,
            'transmission_start_delay': transmission_start_delay_uS/10**6,
            'transmission_delay': transmission_delay_uS/10**6
        }
        return overheads



    def getPacketSize(self):
        '''
            Get the size used for packets in bytes.
        '''
        self.camera.Open()
        packet_size = self.camera.GevSCPSPacketSize.GetValue()
        self.camera.Close()
        return packet_size

    def getPayloadSize(self):
        '''
            Size of payload in bytes, a function of AOI and pixel format.
        '''
        self.camera.Open()
        payload = self.camera.PayloadSize.GetValue()
        self.camera.Close()
        return payload

    def getPixelFormat(self):
        self.camera.Open()
        pixel_format = self.camera.PixelFormat.GetValue()
        self.camera.Close()
        return pixel_format

    def getReadoutTime(self):
        self.camera.Open()
        time = self.camera.ReadoutTimeAbs.GetValue()
        self.camera.Close()
        return time

    def getTemperature(self, sensor_name='Coreboard'):
        self.camera.Open()
        self.camera.TemperatureSelector.SetValue(sensor_name)
        temp = self.camera.TemperatureAbs.GetValue()
        self.camera.Close()
        return temp      

    def getTemperatureState(self, sensor_name='Coreboard'):
        self.camera.Open()
        self.camera.TemperatureSelector.SetValue(sensor_name)
        state = self.camera.TemperatureState.GetValue()
        self.camera.Close()
        return state

    def getThroughputCurrent(self):
        '''
            Device current throughput in bytes/s. Dependent on network.
        '''
        self.camera.Open()
        throughput = self.camera.GevSCDCT.GetValue()
        self.camera.Close()
        return throughput

    def getThroughputCurrent(self):
        '''
            Device max throughput in bytes/s. Not dependent on network.
        '''
        self.camera.Open()
        throughput = self.camera.GevSCDMT.GetValue()
        self.camera.Close()
        return throughput

    def getTransmissionStartDelay(self):
        '''
            Get the time between reading out and transmitting the frame 
            to the host in ticks.
        '''
        self.camera.Open()
        delay = self.camera.GevSCFTD.GetValue()
        self.camera.Close()      
        return delay 

    def readNImagesFromBuffer(self, n_images=1, read_timeout_S=5, 
        time_between_read_attempts_S=0):
        imgs = []
        last_error_code = None
        while self.camera.IsGrabbing():
            try:
                grabResult = self.camera.RetrieveResult(
                    int(read_timeout_S*10**3), 
                    pylon.TimeoutHandling_ThrowException)
                last_error_code = grabResult.GetErrorCode()
                if grabResult.GrabSucceeded():
                    imgs.append(grabResult.Array)
            except genicam.GenericException as e:
                last_error_code = -1
            time.sleep(time_between_read_attempts_S)
            if grabResult is not None:
                grabResult.Release()  
        return imgs, last_error_code

    def setAOI(self, w, h, x_offset, y_offset):
        self.camera.Open()
        self.camera.Width.SetValue(w)
        self.camera.Height.SetValue(h)
        self.camera.OffsetX.SetValue(x_offset)
        self.camera.OffsetY.SetValue(y_offset)
        self.camera.Close()    

    def setAcquisitionMode(self, mode='Continuous'):
        '''
            Set when the camera stops waiting for triggers.

            Can be 'Continuous' or 'SingleFrame'.
        '''
        self.camera.Open()
        success = self.camera.AcquisitionMode.SetValue('Continuous')
        self.camera.Close()
        return success

    def setBinningHorizontal(self, binning):
        self.camera.Open()
        success = self.camera.BinningHorizontal.SetValue(binning)
        self.camera.Close()
        return success

    def setBinningHorizontalMode(self, mode):
        self.camera.Open()
        success = self.camera.BinningHorizontalMode.SetValue(mode)
        self.camera.Close()
        return success

    def setBinningVertical(self, binning):
        self.camera.Open()
        success = self.camera.BinningVertical.SetValue(binning)
        self.camera.Close()
        return success

    def setBinningVerticalMode(self, mode):
        self.camera.Open()
        success = self.camera.BinningVerticalMode.SetValue(mode)
        self.camera.Close()
        return success

    def setBlackLevel(self, level):
        self.camera.Open()
        success = self.camera.BlackLevelRaw.SetValue(level)
        self.camera.Close()
        return success  

    def setExposureTimeMicroseconds(self, exposure_time):
        self.camera.Open()
        success = self.camera.ExposureTimeAbs.SetValue(exposure_time)
        self.camera.Close()
        return success

    def setFrameRate(self, frame_rate):
        '''
            Force frame rate (frames/s) to be a certain value. 0 turns this 
            off.
        '''
        self.camera.Open()
        if frame_rate == 0:
            success = self.camera.AcquisitionFrameRateEnable.SetValue(False)
        else:
            self.camera.AcquisitionFrameRateEnable.SetValue(True)
            success = self.camera.AcquisitionFrameRateAbs.SetValue(frame_rate)
        self.camera.Close()
        return success

    def setGain(self, gain):
        self.camera.Open()
        success = self.camera.GainRaw.SetValue(gain)
        self.camera.Close()        
        return success   

    def setGainAuto(self, gain_auto='Off'):
        self.camera.Open()
        success = self.camera.GainAuto.SetValue(gain_auto)
        self.camera.Close()
        return success            

    def setImageFlipX(self, flip):
        self.camera.Open()
        success = self.camera.ReverseX.SetValue(flip)
        self.camera.Close()        
        return success

    def setImageFlipY(self, flip):
        self.camera.Open()
        success = self.camera.ReverseY.SetValue(flip)
        self.camera.Close()    
        return success

    def setIPD(self, delay):
        '''
            Set delay between sending packets in ticks.
        '''
        self.camera.Open()
        success = self.camera.GevSCPD.SetValue(delay)
        self.camera.Close() 
        return success   

    def setMaxNumBuffers(self, max_num_buffers=25):
        self.camera.Open()
        success = self.camera.MaxNumBuffer.SetValue(max_num_buffers)
        self.camera.Close()
        return success

    def setPacketSize(self, size):
        '''
            Set the size used for packets in bytes.
        '''
        self.camera.Open()
        success = self.camera.GevSCPSPacketSize.SetValue(size)
        self.camera.Close()
        return success

    def setPixelFormat(self, pixel_format='Mono12'):
        self.camera.Open()
        success = self.camera.PixelFormat.SetValue(pixel_format)
        self.camera.Close()
        return success

    def SetTransmissionStartDelay(self, delay):
        '''
            Set the time between reading out and transmitting the frame to 
            the host in ticks.
        '''
        self.camera.Open()
        success = self.camera.GevSCFTD.SetValue(delay)
        self.camera.Close()      
        return success   
       






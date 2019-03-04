import time

import cv2
from pypylon import pylon
from pypylon import genicam

from .cameras import camera

class Basler(camera):
    def __init__(self):
        super(Basler, self).__init__()

    def connect(self):
        """ Open connection to a camera. """
        try:
            assert self.camera is not None
            self.camera.Open()
        except AssertionError:
            raise Exception("No camera is currently defined. You may need " + 
            "to run find() first.")   

    def disconnect(self):
        """ Disconnect from a camera. """
        try:
            assert self.camera is not None
            self.camera.Close()
        except AssertionError:
            raise Exception("No camera is currently defined.")       

    def find(self, serial_number=None, assign=True):
        """ Find a camera.

        The search can be conducted with or without a serial number. If 
        [serial_number] is not specified, the routine will return the first 
        available camera.

        If [assign] is set to True, the returned camera will be assigned to 
        [self.camera].
        """
        tlFactory = pylon.TlFactory.GetInstance()
        devices = tlFactory.EnumerateDevices()
        try:
            if serial_number is not None:
                for i, dev in enumerate(devices):
                    if int(dev.GetSerialNumber()) == int(serial_number):
                        camera = pylon.InstantCamera(
                            tlFactory.CreateDevice(devices[i]))
                        break
            else:
                if len(devices) > 0:
                    camera = pylon.InstantCamera(
                        pylon.TlFactory.GetInstance().CreateFirstDevice())
            assert camera is not None
        except:
            raise Exception("Failed to find camera.")

        if assign:
            self.camera = camera

    def getAcquisitionMode(self):
        """ Get when the camera stops waiting for triggers. """
        self.camera.Open()
        mode = self.camera.AcquisitionMode.GetValue('Continuous')
        self.camera.Close()
        return mode

    def getAOI(self):
        """ Get the area of interest.

        The area of interest is defined by an offset in x, offset in y, width 
        and height.
        """
        try:
            assert self.camera is not None
            self.camera.connect()
            x_offset = self.camera.OffsetX.GetValue()
            y_offset = self.camera.OffsetY.GetValue()
            w = self.camera.Width.GetValue()
            h = self.camera.Height.GetValue()
            self.camera.disconnect()    
            return (w, h, x_offset, y_offset)
        except AssertionError:
            raise Exception("No camera is currently defined.")
        except:
            return None            

    def getBandwidthAssigned(self):
        """ Return the bandwidth assigned to the camera in bytes/s. """
        try:
            assert self.camera is not None
            self.camera.connect()
            bwa = self.camera.GevSCBWA.GetValue()
            self.camera.disconnect()
            return bwa
        except AssertionError:
            raise Exception("No camera is currently defined.")
        except:
            return None

    def getBandwidthReserve(self):
        """ Return the % of bwa reserved to resend packets. """
        self.camera.Open()
        bwr = self.camera.GevSCBWRA.GetValue()
        self.camera.Close()
        return bwr
       
    def getBinningHorizontal(self):
        """ Return the horizontal binning factor. """
        self.camera.Open()
        binning = self.camera.BinningHorizontal.GetValue()
        self.camera.Close()
        return binning

    def getBinningHorizontalMode(self):
        """ Return the horizontal binning mode. """
        self.camera.Open()
        mode = self.camera.BinningHorizontalMode.GetValue()
        self.camera.Close()
        return mode        

    def getBinningVertical(self):
        """ Return the vertical binning factor. """
        self.camera.Open()
        binning = self.camera.BinningVertical.GetValue()
        self.camera.Close()
        return binning

    def getBinningVerticalMode(self):
        """ Return the vertical binning mode. """
        self.camera.Open()
        mode = self.camera.BinningVerticalMode.GetValue()
        self.camera.Close()
        return mode        

    def getBlackLevel(self):
        """ Return the DC bias level. """
        self.camera.Open()
        level = self.camera.BlackLevelRaw.GetValue()
        self.camera.Close()
        return level  

    def getExposureTimeMicroseconds(self):
        """ Return the exposure time in microseconds. """
        self.camera.Open()
        exposure_time = self.camera.ExposureTimeAbs.GetValue()
        self.camera.Close()
        return exposure_time

    def getFrameRate(self):
        """ Return the frame rate. """
        self.camera.Open()
        frame_rate = self.camera.ResultingFrameRateAbs.GetValue()
        self.camera.Close()      
        return frame_rate 

    def getGain(self):
        """ Return the gain. """
        self.camera.Open()
        gain = self.camera.GainRaw.GetValue()
        self.camera.Close()
        return gain

    def getGainAuto(self):
        """ Return the automatic gain mode. """
        self.camera.Open()
        gain = self.camera.GainAuto.GetValue()
        self.camera.Close()
        return gain                    

    def getImageFlipX(self):
        """ Return the x-axis flipping mode. """
        self.camera.Open()
        flip = self.camera.ReverseX.GetValue()
        self.camera.Close()      
        return flip

    def getImageFlipY(self):
        """ Return the y-axis flipping mode. """
        self.camera.Open()
        flip = self.camera.ReverseY.GetValue()
        self.camera.Close() 
        return flip    

    def getIPD(self):
        """ Return delay between sending packets in ticks. """
        self.camera.Open()
        delay = self.camera.GevSCPD.GetValue()
        self.camera.Close() 
        return delay          

    def getMaxNumBuffers(self):
        """ Return the maximum number of buffers available. """
        self.camera.Open()
        max_num_buffers = self.camera.MaxNumBuffer.GetValue()
        self.camera.Close()
        return max_num_buffers  

    def getFrameOverheadsSeconds(self):
        """ Return the frame overhead in seconds.

            The overhead is broken down as follows:
                - delay between triggering and start (exposure_start_delay),
                - time to readout (readout_time)
                - time between reading out and transmitting 
                (transmission_start_delay)
                - time to transfer frame to host (transmission_delay)
        """
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
        """ Return the size used for packets in bytes. """
        self.camera.Open()
        packet_size = self.camera.GevSCPSPacketSize.GetValue()
        self.camera.Close()
        return packet_size

    def getPayloadSize(self):
        """ Return the size of the payload in bytes, a function of AOI and 
        pixel format.
        """
        self.camera.Open()
        payload = self.camera.PayloadSize.GetValue()
        self.camera.Close()
        return payload

    def getPixelFormat(self):
        """ Return the pixel format. """
        self.camera.Open()
        pixel_format = self.camera.PixelFormat.GetValue()
        self.camera.Close()
        return pixel_format

    def getReadoutTime(self):
        """ Return the readout time. """
        self.camera.Open()
        time = self.camera.ReadoutTimeAbs.GetValue()
        self.camera.Close()
        return time

    def getTemperature(self, sensor_name='Coreboard'):
        """ Return a temperature measurement. """
        self.camera.Open()
        self.camera.TemperatureSelector.SetValue(sensor_name)
        temp = self.camera.TemperatureAbs.GetValue()
        self.camera.Close()
        return temp      

    def getTemperatureState(self, sensor_name='Coreboard'):
        """ Return the detector's temperature state. """
        self.camera.Open()
        self.camera.TemperatureSelector.SetValue(sensor_name)
        state = self.camera.TemperatureState.GetValue()
        self.camera.Close()
        return state

    def getThroughputCurrent(self):
        """ Return the current device throughput in bytes/s. """
        self.camera.Open()
        throughput = self.camera.GevSCDCT.GetValue()
        self.camera.Close()
        return throughput

    def getTransmissionStartDelay(self):
        """ Get the time between reading out and transmitting the frame to 
        the host in ticks.
        """
        self.camera.Open()
        delay = self.camera.GevSCFTD.GetValue()
        self.camera.Close()      
        return delay 

    def read(self, n_images=1, read_timeout_ms=1000, 
        grab_timeout_ms=100, max_grab_attempts=3, grab_strategy='OneByOne'):
        """ Read a frame(s) from the detector. 
        
        If [grab_strategy] is set to 'OneByOne' [n_frames] will be 
        returned. If it's set to 'LatestImageOnly', [n_frames] will be 
        ignored and a single frame will be returned.
        """
        if grab_strategy == 'OneByOne':
            imgs = []
            grab_attempts = 0
            while len(imgs) < n_images:
                if grab_attempts >= max_grab_attempts:
                    break
                else:
                    if not self.camera.IsGrabbing():
                        self.camera.StartGrabbingMax(
                            n_images-len(imgs), 
                            pylon.GrabStrategy_OneByOne)
                    if self.camera.GetGrabResultWaitObject().Wait(
                        grab_timeout_ms):
                        grabResult = self.camera.RetrieveResult(
                            read_timeout_ms, pylon.TimeoutHandling_Return)
                        if grabResult.IsValid() and \
                        grabResult.GrabSucceeded():
                            imgs.append(grabResult.Array)
                            grabResult.Release()
                    grab_attempts += 1
            return imgs
        elif grab_strategy == 'LatestImageOnly':
            img = None
            grab_attempts = 0
            while img is None:
                if grab_attempts >= max_grab_attempts:
                    break
                else:
                    if not self.camera.IsGrabbing():
                        self.camera.StartGrabbing(
                            pylon.GrabStrategy_LatestImageOnly)
                    if self.camera.GetGrabResultWaitObject().Wait(
                        grab_timeout_ms):                      
                        grabResult = self.camera.RetrieveResult(
                            read_timeout_ms, pylon.TimeoutHandling_Return)
                        if grabResult.IsValid() and \
                        grabResult.GrabSucceeded():
                            img = grabResult.Array
                        grabResult.Release()
                        grab_attempts += 1
            return img

    def setAOI(self, w, h, x_offset, y_offset):
        """ Set the area of interest.

        The area of interest is defined by an offset in x, offset in y, width 
        and height.
        """
        self.camera.Open()
        try:
            self.camera.Width.SetValue(w)
            self.camera.Height.SetValue(h)
            self.camera.OffsetX.SetValue(x_offset)
            self.camera.OffsetY.SetValue(y_offset)
        except genicam.OutOfRangeException:
            self.camera.OffsetX.SetValue(x_offset)
            self.camera.OffsetY.SetValue(y_offset)
            self.camera.Width.SetValue(w)
            self.camera.Height.SetValue(h)
        self.camera.Close()    

    def setAcquisitionMode(self, mode='Continuous'):
        """ Set when the camera stops waiting for triggers.

        Can be 'Continuous' or 'SingleFrame'.
        """
        self.camera.Open()
        success = self.camera.AcquisitionMode.SetValue(mode)
        self.camera.Close()
        return success

    def setBinningHorizontal(self, binning):
        """ Set the horizontal binning factor. """
        self.camera.Open()
        success = self.camera.BinningHorizontal.SetValue(binning)
        self.camera.Close()
        return success

    def setBinningHorizontalMode(self, mode):
        # This is overriden for different camera models as the 
        # function call is different.
        pass

    def setBinningVertical(self, binning):
        """ Set the vertical binning factor. """
        self.camera.Open()
        success = self.camera.BinningVertical.SetValue(binning)
        self.camera.Close()
        return success

    def setBinningVerticalMode(self, mode):
        # This is overriden for different camera models as the 
        # function call is different.
        pass  

    def setBlackLevel(self, level):
        """ Set the DC bias level. """
        self.camera.Open()
        success = self.camera.BlackLevelRaw.SetValue(level)
        self.camera.Close()
        return success  

    def setExposureTimeMicroseconds(self, exposure_time):
        """ Set the exposure time in microseconds. """
        self.camera.Open()
        success = self.camera.ExposureTimeAbs.SetValue(exposure_time)
        self.camera.Close()
        return success

    def setFrameRate(self, frame_rate):
        """ Force frame rate (frames/s) to be a certain value. 
        
        0 turns this off.
        """
        self.camera.Open()
        if frame_rate == 0:
            success = self.camera.AcquisitionFrameRateEnable.SetValue(False)
        else:
            self.camera.AcquisitionFrameRateEnable.SetValue(True)
            success = self.camera.AcquisitionFrameRateAbs.SetValue(frame_rate)
        self.camera.Close()
        return success

    def setGain(self, gain):
        """ Set the gain. """
        self.camera.Open()
        success = self.camera.GainRaw.SetValue(gain)
        self.camera.Close()        
        return success   

    def setGainAuto(self, gain_auto='Off'):
        """ Set the automatic gain mode. """
        self.camera.Open()
        success = self.camera.GainAuto.SetValue(gain_auto)
        self.camera.Close()
        return success            

    def setImageFlipX(self, flip):
        """ Set the x-axis flipping mode. """
        self.camera.Open()
        success = self.camera.ReverseX.SetValue(flip)
        self.camera.Close()        
        return success

    def setImageFlipY(self, flip):
        """ Set the y-axis flipping mode. """
        self.camera.Open()
        success = self.camera.ReverseY.SetValue(flip)
        self.camera.Close()    
        return success

    def setIPD(self, delay):
        """ Set delay between sending packets in ticks. """ 
        self.camera.Open()
        success = self.camera.GevSCPD.SetValue(delay)
        self.camera.Close() 
        return success   

    def setMaxNumBuffers(self, max_num_buffers=25):
        """ Set the maximum number of buffers available. """
        self.camera.Open()
        success = self.camera.MaxNumBuffer.SetValue(max_num_buffers)
        self.camera.Close()
        return success

    def setPacketSize(self, size):
        """ Set the packet size in bytes. """
        self.camera.Open()
        success = self.camera.GevSCPSPacketSize.SetValue(size)
        self.camera.Close()
        return success

    def setPixelFormat(self, pixel_format='Mono12'):
        self.camera.Open()
        success = self.camera.PixelFormat.SetValue(pixel_format)
        self.camera.Close()
        return success

    def setTransmissionStartDelay(self, delay):
        '''
            Set the time between reading out and transmitting the frame to 
            the host in ticks.
        '''
        self.camera.Open()
        success = self.camera.GevSCFTD.SetValue(delay)
        self.camera.Close()      
        return success   

class Basler_2040_35gm(Basler):
    def __init__(self):
        super(Basler_2040_35gm, self).__init__()
    
    def setBinningHorizontalMode(self, mode):
        """ Set the horizontal binning mode. """
        self.camera.Open()
        success = self.camera.BinningHorizontalMode.SetValue(mode)
        self.camera.Close()
        return success

    def setBinningVerticalMode(self, mode):
        """ Set the vertical binning mode. """
        self.camera.Open()
        success = self.camera.BinningVerticalMode.SetValue(mode)
        self.camera.Close()
        return success

class Basler_1600_60gm(Basler):
    def __init__(self):
        super(Basler_1600_60gm, self).__init__()
    
    def setBinningHorizontalMode(self, mode):
        """ Set the horizontal binning mode. """
        self.camera.Open()
        success = self.camera.BinningModeHorizontal.SetValue(mode)
        self.camera.Close()
        return success

    def setBinningVerticalMode(self, mode):
        """ Set the vertical binning mode. """
        self.camera.Open()
        success = self.camera.BinningModeVertical.SetValue(mode)
        self.camera.Close()
        return success






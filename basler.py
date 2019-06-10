import time

import cv2
from pypylon import pylon
from pypylon import genicam

try:
    from .cameras import camera
except ModuleNotFoundError:
    from cameras import camera

class Basler(camera):
    def __init__(self):
        super(Basler, self).__init__()

    def beginExpose(self, grab_strategy='LatestImageOnly'):
        try:
            self.connect()
            self.grab_strategy = grab_strategy
            if self.grab_strategy == 'OneByOne':   
                rtn = self.camera.StartGrabbing(
                    pylon.GrabStrategy_OneByOne)
                
            elif self.grab_strategy == 'LatestImageOnly':
                rtn = self.camera.StartGrabbing(
                    pylon.GrabStrategy_LatestImageOnly)
        except:
            rtn = None
        return rtn

    def connect(self):
        """ Open connection to a camera. """
        try:
            assert self.camera is not None
            if not self.camera.IsOpen():
                rtn = self.camera.Open()
            else:
                rtn = True
        except AssertionError:
            raise Exception("No camera is currently defined. You may need " + 
            "to run find() first.")  
            rtn = None
        return rtn 

    def disconnect(self):
        """ Disconnect from a camera. """
        try:
            assert self.camera is not None
            if self.camera.IsOpen():
                rtn = self.camera.Close()
            else:
                rtn = True
        except AssertionError:
            raise Exception("No camera is currently defined.")   
            rtn = None    
        return rtn

    def endExpose(self):
        try:
            self.connect()
            rtn = self.camera.StopGrabbing()
            self.grab_strategy = None
        except:
            rtn = None
        return rtn

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
        try:
            self.connect()
            rtn = self.camera.AcquisitionMode.GetValue('Continuous')
        except:
            rtn = None
        return rtn

    def getAOI(self):
        """ Get the area of interest.

        The area of interest is defined by an offset in x, offset in y, width 
        and height.
        """
        try:
            self.connect()
            x_offset = self.camera.OffsetX.GetValue()
            y_offset = self.camera.OffsetY.GetValue()
            w = self.camera.Width.GetValue()
            h = self.camera.Height.GetValue()   
            rtn = (w, h, x_offset, y_offset)
        except:
            rtn = None
        return rtn            

    def getBandwidthAssigned(self):
        """ Return the bandwidth assigned to the camera in bytes/s. """
        try:
            self.connect()
            rtn = self.camera.GevSCBWA.GetValue()
        except:
            rtn = None
        return rtn

    def getBandwidthReserve(self):
        """ Return the % of bwa reserved to resend packets. """
        try:
            self.connect()
            rtn = self.camera.GevSCBWRA.GetValue()
        except:
            rtn = None
        return rtn
       
    def getBinningHorizontal(self):
        """ Return the horizontal binning factor. """
        try:
            self.connect()
            rtn = self.camera.BinningHorizontal.GetValue()
        except:
            rtn = None
        return rtn

    def getBinningHorizontalMode(self):
        """ Return the horizontal binning mode. """
        try:
            self.connect()
            rtn = self.camera.BinningHorizontalMode.GetValue()
        except:
            rtn = None
        return rtn        

    def getBinningVertical(self):
        """ Return the vertical binning factor. """
        try:
            self.connect()
            rtn = self.camera.BinningVertical.GetValue()
        except:
            rtn = None
        return rtn

    def getBinningVerticalMode(self):
        """ Return the vertical binning mode. """
        try:
            self.connect()
            rtn = self.camera.BinningVerticalMode.GetValue()
        except:
            rtn = None
        return rtn        

    def getBlackLevel(self):
        """ Return the DC bias level. """
        try:
            self.connect()
            rtn = self.camera.BlackLevelRaw.GetValue()
        except:
            rtn = None
        return rtn

    def getDeviceUserID(self):
        """ Return the device ID. """
        try:
            self.connect()
            rtn = self.camera.DeviceUserID.GetValue()
        except:
            rtn = None
        return rtn          

    def getExposureTimeMicroseconds(self):
        """ Return the exposure time in microseconds. """
        try:
            self.connect()
            rtn = self.camera.ExposureTimeAbs.GetValue()
        except:
            rtn = None
        return rtn

    def getFrameRate(self):
        """ Return the frame rate. """
        try:
            self.connect()
            rtn = self.camera.ResultingFrameRateAbs.GetValue()
        except: 
            rtn = None     
        return rtn 

    def getGain(self):
        """ Return the gain. """
        try:
            self.connect()
            rtn = self.camera.GainRaw.GetValue()
        except:
            rtn = None
        return rtn

    def getGainAuto(self):
        """ Return the automatic gain mode. """
        try:
            self.connect()
            rtn = self.camera.GainAuto.GetValue()
        except:
            rtn = None
        return rtn                    

    def getImageFlipX(self):
        """ Return the x-axis flipping mode. """
        try:
            self.connect()
            rtn = self.camera.ReverseX.GetValue()
        except:
            rtn = None   
        return rtn

    def getImageFlipY(self):
        """ Return the y-axis flipping mode. """
        try:
            self.connect()
            rtn = self.camera.ReverseY.GetValue()
        except:
            rtn = None 
        return rtn    

    def getIPD(self):
        """ Return delay between sending packets in ticks. """
        try:
            self.connect()
            rtn = self.camera.GevSCPD.GetValue()
        except:
            rtn = None
        return rtn          

    def getMaxNumBuffers(self):
        """ Return the maximum number of buffers available. """
        try:
            self.connect()
            rtn = self.camera.MaxNumBuffer.GetValue()
        except:
            rtn = None
        return rtn  

    def getFrameOverheadsSeconds(self):
        """ Return the frame overhead in seconds.

            The overhead is broken down as follows:
                - delay between triggering and start (exposure_start_delay),
                - time to readout (readout_time)
                - time between reading out and transmitting 
                (transmission_start_delay)
                - time to transfer frame to host (transmission_delay)
        """
        try:
            transmission_delay_uS = self.getPayloadSize()/\
                self.getThroughputCurrent()*10**6
            transmission_start_delay_uS = self.getTransmissionStartDelay()       
            readout_time_uS = self.getReadoutTime()       
            rtn = {
                'exposure_start_delay': self.exposure_start_delay_uS/10**6,
                'readout_time': readout_time_uS/10**6,
                'transmission_start_delay': transmission_start_delay_uS/10**6,
                'transmission_delay': transmission_delay_uS/10**6
            }
        except:
            rtn = None
        return rtn

    def getPacketSize(self):
        """ Return the size used for packets in bytes. """
        try:
            self.connect()
            rtn = self.camera.GevSCPSPacketSize.GetValue()
        except:
            rtn = None
        return rtn

    def getPayloadSize(self):
        """ Return the size of the payload in bytes, a function of AOI and 
        pixel format.
        """
        try:
            self.connect()
            rtn = self.camera.PayloadSize.GetValue()
        except:
            rtn = None
        return rtn

    def getPixelFormat(self):
        """ Return the pixel format. """
        try:
            self.connect()
            rtn = self.camera.PixelFormat.GetValue()
        except:
            rtn = None
        return rtn

    def getReadoutTime(self):
        """ Return the readout time. """
        try:
            self.connect()
            rtn = self.camera.ReadoutTimeAbs.GetValue()
        except:
            rtn = None
        return rtn

    def getTemperature(self, sensor_name='Coreboard'):
        """ Return a temperature measurement. """
        try:
            self.connect()
            self.camera.TemperatureSelector.SetValue(sensor_name)
            rtn = self.camera.TemperatureAbs.GetValue()
        except:
            rtn = None
        return rtn      

    def getTemperatureState(self, sensor_name='Coreboard'):
        """ Return the detector's temperature state. """
        try:
            self.connect()
            rtn = self.camera.TemperatureState.GetValue()
        except:
            rtn = None
        return rtn

    def getThroughputCurrent(self):
        """ Return the current device throughput in bytes/s. """
        try:
            self.connect()
            rtn = self.camera.GevSCDCT.GetValue()
        except:
            rtn = None
        return rtn

    def getTransmissionStartDelay(self):
        """ Get the time between reading out and transmitting the frame to 
        the host in ticks.
        """
        try:
            self.connect()
            rtn = self.camera.GevSCFTD.GetValue()
        except:
            rtn = None    
        return rtn 

    def isExposing(self):
        try:
            if self.camera.IsGrabbing():
                rtn = True
            else:
                rtn = False
        except:
            rtn = None
        return rtn

    def read(self, n_images=1, read_timeout_ms=1000, max_grab_attempts=3):
        """ Read a frame(s) from the detector. 
        """
        imgs = []
        grab_attempts = 0
        while len(imgs) < n_images:
            if grab_attempts >= max_grab_attempts:
                break
            else:
                grabResult = self.camera.RetrieveResult(
                    read_timeout_ms, pylon.TimeoutHandling_Return)
                if grabResult.IsValid() and \
                grabResult.GrabSucceeded():
                    imgs.append(grabResult.Array)
                    grabResult.Release()
                grab_attempts += 1
        return imgs

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
        try:
            packet_size = int(
                config['PACKET_SIZE'])
        except KeyError:
            packet_size = None               

        if self.camera is not None:
            if exptime is not None:
                self.setExposureTimeMicroseconds(exptime)
            if pixel_format is not None:
                self.setPixelFormat(pixel_format)

            # We need to set binning first, then adjust AOI.
            #
            current_binning_h = self.getBinningHorizontal()
            current_binning_v = self.getBinningVertical()
            if binning_h is not None:
                self.setBinningHorizontal(binning_h)
            if binning_v is not None:
                self.setBinningVertical(binning_v)
            if width is not None and height is not None and \
            x_offset is not None and y_offset is not None:
                self.setAOI(width, height, x_offset, y_offset)

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
            if packet_size is not None:
                self.setPacketSize(packet_size)

    def setAOI(self, w, h, x_offset, y_offset):
        """ Set the area of interest.

        The area of interest is defined by an offset in x, offset in y, width 
        and height.
        """
        try:
            self.connect()
            rtn = self.camera.OffsetX.SetValue(0)      
            rtn = self.camera.OffsetY.SetValue(0)     
            rtn = self.camera.Width.SetValue(1)       
            rtn = self.camera.Height.SetValue(1)       
            rtn = self.camera.OffsetX.SetValue(x_offset)     
            rtn = self.camera.OffsetY.SetValue(y_offset)      
            rtn = self.camera.Width.SetValue(w)      
            rtn = self.camera.Height.SetValue(h)
        except:
            rtn = None
        return rtn

    def setAcquisitionMode(self, mode='Continuous'):
        """ Set when the camera stops waiting for triggers.

        Can be 'Continuous' or 'SingleFrame'.
        """
        try:
            self.connect()
            rtn = self.camera.AcquisitionMode.SetValue(mode)
        except:
            rtn = None
        return rtn

    def setBinningHorizontal(self, binning):
        """ Set the horizontal binning factor. """
        try:
            self.connect()
            rtn = self.camera.BinningHorizontal.SetValue(binning)
        except:
            rtn = None
        return rtn

    def setBinningHorizontalMode(self, mode):
        # This is overriden for different camera models as the 
        # function call is different.
        pass

    def setBinningVertical(self, binning):
        """ Set the vertical binning factor. """
        try:
            self.connect()
            rtn = self.camera.BinningVertical.SetValue(binning)
        except:
            rtn = None
        return rtn

    def setBinningVerticalMode(self, mode):
        # This is overriden for different camera models as the 
        # function call is different.
        pass  

    def setBlackLevel(self, level):
        """ Set the DC bias level. """
        try:
            self.connect()
            rtn = self.camera.BlackLevelRaw.SetValue(level)
        except:
            rtn = None
        return rtn  

    def setDeviceUserID(self, did):
        """ Set the device ID (16 char) """
        try:
            self.connect()
            rtn = self.camera.DeviceUserID.SetValue(did)
        except:
            rtn = None
        return rtn  

    def setExposureTimeMicroseconds(self, exposure_time):
        """ Set the exposure time in microseconds. """
        try:
            self.connect()
            rtn = self.camera.ExposureTimeAbs.SetValue(exposure_time)
        except:
            rtn = None
        return rtn

    def setFrameRate(self, frame_rate):
        """ Force frame rate (frames/s) to be a certain value. 
        
        0 turns this off.
        """
        try:
            self.connect()
            if frame_rate == 0:
                rtn = self.camera.AcquisitionFrameRateEnable.SetValue(
                    False)
            else:
                self.camera.AcquisitionFrameRateEnable.SetValue(True)
                rtn = self.camera.AcquisitionFrameRateAbs.SetValue(
                    frame_rate)
        except:
            rtn = None
        return rtn

    def setGain(self, gain):
        """ Set the gain. """
        try:
            self.connect()
            rtn = self.camera.GainRaw.SetValue(gain)
        except:
            rtn = None     
        return rtn   

    def setGainAuto(self, gain_auto='Off'):
        """ Set the automatic gain mode. """
        try:
            self.connect()
            rtn = self.camera.GainAuto.SetValue(gain_auto)
        except:
            rtn = None
        return rtn            

    def setImageFlipX(self, flip):
        """ Set the x-axis flipping mode. """
        try:
            self.connect()
            rtn = self.camera.ReverseX.SetValue(flip)
        except:
            rtn = None      
        return rtn

    def setImageFlipY(self, flip):
        """ Set the y-axis flipping mode. """
        try:
            self.connect()
            rtn = self.camera.ReverseY.SetValue(flip)
        except:
            rtn = None   
        return rtn

    def setIPD(self, delay):
        """ Set delay between sending packets in ticks. """ 
        try:
            self.connect()
            rtn = self.camera.GevSCPD.SetValue(delay)
        except:
            rtn = None 
        return rtn   

    def setMaxNumBuffers(self, max_num_buffers=25):
        """ Set the maximum number of buffers available. """
        try:
            self.connect()
            rtn = self.camera.MaxNumBuffer.SetValue(max_num_buffers)
        except:
            rtn = None
        return rtn

    def setPacketSize(self, size):
        """ Set the packet size in bytes. """
        try:
            self.connect()
            rtn = self.camera.GevSCPSPacketSize.SetValue(size)
        except:
            rtn = None
        return rtn

    def setPixelFormat(self, pixel_format='Mono12'):
        try:
            self.connect()
            rtn = self.camera.PixelFormat.SetValue(pixel_format)
        except:
            rtn = None
        return rtn

    def setTransmissionStartDelay(self, delay):
        """ Set the time between reading out and transmitting the frame to 
            the host in ticks.
        """
        try:
            self.connect()
            rtn = self.camera.GevSCFTD.SetValue(delay)
        except:
            rtn = None      
        return rtn   

class Basler_2040_35gm(Basler):
    def __init__(self):
        super(Basler_2040_35gm, self).__init__()
    
    def setBinningHorizontalMode(self, mode):
        """ Set the horizontal binning mode. """
        try:
            self.connect()
            rtn = self.camera.BinningHorizontalMode.SetValue(mode)
        except:
            rtn = None
        return rtn

    def setBinningVerticalMode(self, mode):
        """ Set the vertical binning mode. """
        try:
            self.connect()
            rtn = self.camera.BinningVerticalMode.SetValue(mode)
        except:
            rtn = None
        return rtn

class Basler_1600_60gm(Basler):
    def __init__(self):
        super(Basler_1600_60gm, self).__init__()
    
    def setBinningHorizontalMode(self, mode):
        """ Set the horizontal binning mode. """
        try:
            self.connect()
            rtn = self.camera.BinningModeHorizontal.SetValue(mode)
        except:
            rtn = None
        return rtn

    def setBinningVerticalMode(self, mode):
        """ Set the vertical binning mode. """
        try:
            self.connect()
            rtn = self.camera.BinningModeVertical.SetValue(mode)
        except:
            rtn = None
        return rtn


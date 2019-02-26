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

    '''def beginExpose(self, max_number_of_exposures=0):
        if max_number_of_exposures == 0:
            self.camera.StartGrabbing() 
        else:
            self.camera.StartGrabbingMax(max_number_of_exposures)'''

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
        """ Get the bandwidth assigned to camera in bytes/s. """
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

    def getTransmissionStartDelay(self):
        '''
            Get the time between reading out and transmitting the frame 
            to the host in ticks.
        '''
        self.camera.Open()
        delay = self.camera.GevSCFTD.GetValue()
        self.camera.Close()      
        return delay 

    def readNImagesFromBuffer(self, n_images=1, read_timeout_S=5):
        imgs = []
        last_error_code = None
        while len(imgs)<n_images:
            try:
                assert self.camera.IsGrabbing() == True
            except:
                self.camera.StartGrabbingMax(10000, 
                    pylon.GrabStrategy_OneByOne)
                continue
            try:
                grabResult = self.camera.RetrieveResult(
                    int(read_timeout_S*10**3), 
                    pylon.TimeoutHandling_ThrowException)
                grabResult.GrabSucceeded()
            except:
                continue

            if grabResult.GrabSucceeded():
                imgs.append(grabResult.Array)
                last_error_code = grabResult.GetErrorCode()
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

    def setTransmissionStartDelay(self, delay):
        '''
            Set the time between reading out and transmitting the frame to 
            the host in ticks.
        '''
        self.camera.Open()
        success = self.camera.GevSCFTD.SetValue(delay)
        self.camera.Close()      
        return success   

    def showLiveFeed(self, frame, read_timeout_S, response=None, prnu=None, 
    tcal_StoT=None, ss_calibration_params=None):
        self.showLiveFeed_cursor_x = -1
        self.showLiveFeed_cursor_y = -1
        cv2.setMouseCallback(frame, self.showLiveFeed_callback_mousemove)

        do_inst = False		        # instrument response correction
        do_prnu = False		        # prnu correction
        do_tcal = False		        # temperature calibration
        self.camera.StartGrabbingMax(10000, 
            pylon.GrabStrategy_LatestImageOnly)
        while True:
            try:
                assert self.camera.IsGrabbing() == True
            except:
                self.camera.StartGrabbingMax(10000, 
                    pylon.GrabStrategy_LatestImageOnly)
                continue
            try:
                grabResult = self.camera.RetrieveResult(
                    int(read_timeout_S*10**3), 
                    pylon.TimeoutHandling_ThrowException)
                grabResult.GrabSucceeded()
            except:
                continue
                
            if grabResult.GrabSucceeded():
                img = grabResult.GetArray()
                if do_inst:
                    img = img*response
                if do_prnu:
                    img = img*prnu
                if do_tcal:
                    # gain then offset
                    img = img * ss_calibration_params['gain']
                    img = img + ss_calibration_params['offset']
                    img = tcal_StoT(img)
                self.showLiveFeed_render(
                    img, [self.showLiveFeed_cursor_x, 
                    self.showLiveFeed_cursor_y], 'live', do_inst, do_prnu,
                    do_tcal)
                rtn = self.showLiveFeed_logic(img)
                if rtn == True:
                    break
                if rtn == 48:
                    if response is not None:
                        do_inst = not do_inst
                if rtn == 49:
                    if prnu is not None:
                        do_prnu = not do_prnu
                if rtn == 50:
                    if tcal_StoT is not None \
                    and ss_calibration_params is not None:
                        do_tcal = not do_tcal
            else:
                pass
            if grabResult is not None:
                grabResult.Release() 
        return True

    def showLiveFeed_callback_mousemove(self, event, x, y, flags, params):
        self.showLiveFeed_cursor_x = x
        self.showLiveFeed_cursor_y = y

    def showLiveFeed_logic(self, img):
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            return True
        if k == 48:
            return 48
        if k == 49:
            return 49
        if k == 50:
            return 50
        return False

    def showLiveFeed_render(self, img, cursor_position, frame, do_inst, do_prnu, 
        do_tcal):
        img8 = (img/16).astype('uint8')
        bgr = cv2.cvtColor(img8, cv2.COLOR_GRAY2BGR)

        scale_height = img.shape[1]/cv2.getWindowImageRect(frame)[3]
        scale_width = img.shape[0]/cv2.getWindowImageRect(frame)[2]
        
        x = int(img.shape[0]-(50*scale_width))
        y = int(50*scale_height)
        text = "inst (KP0)"
        if do_inst:
            cv2.putText(bgr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                scale_height, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(bgr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                scale_height, (0, 0, 255), 1, cv2.LINE_AA)

        y += int(50*scale_height)
        text = "prnu (KP1)"
        if do_prnu:
            cv2.putText(bgr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                scale_height, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(bgr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                scale_height, (0, 0, 255), 1, cv2.LINE_AA)

        y += int(50*scale_height)
        text = "tcal (KP2)"
        if do_tcal:
            cv2.putText(bgr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                scale_height, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(bgr, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                scale_height, (0, 0, 255), 1, cv2.LINE_AA)

        #  cursor value
        text = str(round(img[cursor_position[1], cursor_position[0]], 1))
        labelOrigin = (int(round(cursor_position[0] + 20*scale_width)), 
            int(round(cursor_position[1] - 20*scale_height)))

        cv2.putText(bgr, text, labelOrigin, cv2.FONT_HERSHEY_SIMPLEX, scale_height,
            (255, 0, 0), 1, cv2.LINE_AA)

        cv2.imshow(frame, bgr)

class Basler_2040_35gm(Basler):
    def __init__(self):
        super(Basler_2040_35gm, self).__init__()
    






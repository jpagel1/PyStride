"""PyStride - Stride IO Driver - JSP - 3/18/22"""

#Imports
from pymodbus.client import ModbusTcpClient
from time import sleep

class PyStride():
    """Base Class for the Stride"""
    
    def __init__(self, address, nodeID=None):
        """Initialize the Stride"""
        self.client = ModbusTcpClient(host = address,source_address=nodeID)
        
    def connectClient(self):
        """Connect to the Client"""
        if (self.client.is_socket_open()):
            self.client.connect()
        
    def closeClient(self):
        """Close the Client"""
        self.client.close()
        
    def getFirmwareVersion(self):
        """Returns the Firmware Version"""
        rawFirmware = self.client.read_holding_registers(1,2)

        #Take the raw registers and format the version
        word0 = rawFirmware.registers[0]
        word1 = rawFirmware.registers[1]
        str0 = str(hex(word0)).replace('0x','')[0:1]
        str0_1 = str(hex(word0)).replace('0x','')[1:2]
        str1 = str(hex(word1)).replace('0x','')[0:1]
        str1_1 = str(hex(word1)).replace('0x','')[1:2]
        formattedFirmware = str0+'.'+str0_1 + '.' + str1 + '.' + str1_1
        
        return formattedFirmware
    
    def getNodeID(self):
        """Returns the Node ID"""
        rawNodeID = self.client.read_holding_registers(6,1)
        return rawNodeID.registers[0]

    def setWatchdogEnable(self,value):
        """Sets the watchdog to be enabled"""
        self.client.write_coil(160,value)

    def getWatchdogEnable(self):
        """Gets if the Watchdog is enabled"""
        watchDogEnabled = self.client.read_coils(160,1)
        return watchDogEnabled.bits[0]

    def getWatchDogTimer(self):
        """Returns the watchdog timer"""
        rawWatchDogTimer = self.client.read_holding_registers(12,1)
        return rawWatchDogTimer.registers[0]

    def setWatchDogTimer(self,time):
        """Sets the watchdog timer"""
        self.client.write_register(12,time)

    def setWatchdogEvent(self,value):
        """Sets the watchdog event"""
        self.client.write_coil(161,value)

    def getWatchdogEvent(self):
        """Gets the watchdog event"""
        watchDogEvent = self.client.read_coils(161,1)
        return watchDogEvent.bits[0]

    def setPowerUpEvent(self,value):
        """Sets the powerup event status"""
        self.client.write_coil(162,value)
        
    def getPowerUpEvent(self):
        """Gets the powerup event status"""
        powerUpEvent = self.client.read_coils(162,1)
        return powerUpEvent.bits[0]

class PyStrideDigital(PyStride):
    """Digital Version of the PyStride"""

    def __init__(self,address, nodeID=None):
        """Import all methods from the base Pystride"""
        super().__init__(address,nodeID)
        
        #Map Initialize, eventually lets load from a csv if they want to address by name
        self.outputIDs = {0:488,1:489,2:490,3:491,4:492,5:493,6:494,7:495}
        self.inputIDs = {0:504,1:505,2:506,3:507,4:508,5:509,6:510}
        self.inputFreqIDs = {0:34,1:35,2:36,3:37}

    def clearShortCircuitAlarm(self):
        """clears the short circuit alarm"""
        self.client.write_coil(164,False)
        
    def getShortCircuitAlarm(self):
        """Gets the short circuit alarm"""
        shortCircuitAlarm = self.client.read_coils(164,1)
        return shortCircuitAlarm.bits[0]
        
    def setDigitalOutput(self,outputID,value):
        """Set Output On/Off"""
        #Starts at 488 so use ID map from initialize
        coilToWrite = self.outputIDs[outputID]
        self.client.write_coil(coilToWrite,value)

    def getDigitalOutput(self,outputID):
        """Get If Output On/Off"""
        coiltoRead = self.outputIDs[outputID]
        coilVal = self.client.read_coils(coiltoRead,1)
        return coilVal.bits[0]
    
    def getDigitalInput(self,inputID):
        """Get Digital Input Value for ID"""
        coilVal = self.client.read_coils(inputID)
        return coilVal.bits[0]

    def getAllDigitalInputs(self):
        """Get all Digital Inputs as a list"""
        coilL = []
        for value in self.inputIDs.values():
            coilVal = self.client.read_coils(value)
            coilL.append(coilVal.bits[0])
        return coilL
            
        #rawCoils = self.client.read_holding_registers(31,1)
        #print(rawCoils.registers)
        #return rawCoils.registers[0]
    
    def getFrequencyDI(self,inputID):
        """Get the frequency of the DI specified"""
        regtoRead = self.inputFreqIDs[inputID]
        rawCoils = self.client.read_holding_registers(regtoRead,1)
        return rawCoils.registers[0]

class PyStrideAnalog(PyStride):
    """Analog Version of the PyStride - Like MB08ADS"""

    def __init__(self,address, nodeID=None):
        """Import all methods from the base Pystride"""
        super().__init__(address,nodeID)
        
        #Map Initialize, eventually lets load from a csv if they want to address by name
        self.inputAnalogIDs = {0:40,1:41,2:42,3:43,4:44,5:45,6:46,7:47}
    
    def getAnalogInput(self,inputID):
        """Get the uA of the Analog Inputs"""
        regtoRead = self.inputAnalogIDs[inputID]
        rawCoils = self.client.read_holding_registers(regtoRead,1)
        return rawCoils.registers[0]





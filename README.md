# PyStride
Automation Direct Stride IO Driver

Simple Driver to Interface with Automation Direct's Stride IO

Examples (see PyStrideClass for more):
```
#Initialize Communication
StrideIP = '192.168.1.100'
testStride = PyStrideDigital(StrideIP)
testStride.connectClient()

#Test Firmware Version
firmwareVer = testStride.getFirmwareVersion()
print(f"The Firmware Version is: {firmwareVer}")

#Test Node ID
nodeID = testStride.getNodeID()
print(f"The Node ID is: {nodeID}")

#Test watchdog timer
watchdogTimer = testStride.getWatchDogTimer()
print(f"The Watchdog Timer is: {watchdogTimer}") 

#Read In Inputs
digIn = testStride.getAllDigitalInputs()

#Set Digital Output
testStride.setDigitalOutput(0, False)

#Close Communication
testStride.closeClient()
```

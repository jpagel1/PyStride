"""Testing of The PyStride Class with Simple Tank Fill Program"""

from PyStrideClass import PyStrideAnalog,PyStrideDigital
from time import sleep, time

#Simple State Machine Loop to Fill Tank or Something
updateRate = .1 #100 MS Update Rate
pumpOnTime = 0
pumpTimeout = 30
initialT = 0
state = 0
stop = False

while(stop == False):
    """While No Stop Condition Fill The Tank if it is Low"""
    """
        Digital Inputs
        1 - Low Float
        2 - High Float
        3 - Cancel Program
        
        Digital Outputs
        1 - Pump On
    """
    
    if (state == 0):
        """State is 0 so Initialize Communication and Print out Info"""
        
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
        
        #Increment State
        state = 1
        
    if(state == 1):
        """State is 1 so Now lets run the main program"""
        
        #Read In Inputs
        digIn = testStride.getAllDigitalInputs()
        DI_Low_Float = digIn[0]
        DI_High_Float = digIn[1]
        DI_Cancel_Program = digIn[2]
        
        #Read In Output
        pumpOn = testStride.getDigitalOutput(0)
        
        if (pumpOn):
            """If the Pump is On, add time current time to old time"""
            pumpOnTime = time() - initialT
        else:
            pumpOnTime = 0
        
        print(round(pumpOnTime,2))

        if (DI_Cancel_Program):
            """DI Cancel Program Is On so move to final state and cancel out"""
            state = 3
        
        elif (DI_High_Float and state ==1):
            """If DI High Float is On, then Shut off Pump"""
            testStride.setDigitalOutput(0, False)
            
        elif (DI_Low_Float is False and state ==1):
            """Low Float if a NC and is Off so we are low"""
            testStride.setDigitalOutput(0, True)
            
            if (pumpOnTime == 0):
                initialT = time()
            
            #If Pump is on for 30 seconds jump out
            if (pumpOnTime > pumpTimeout):
                state = 3
                print(f"Pump Fill Timeout After {pumpTimeout} Seconds")
            
    if (state ==3):
        """Cancel Out"""
        testStride.setDigitalOutput(0,False)
        sleep(.5)
        testStride.closeClient()
        
        #Jump out while loop
        stop= True

    
    #Wait for Freq Update
    sleep(updateRate)

#Cancel Out if Error Occured
if (testStride.client.connected):
    testStride.closeClient()

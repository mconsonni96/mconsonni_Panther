
# libraries
from time import sleep

import pylibtdc

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



# handler
myBackend = pylibtdc.TDCBackend()
devices = myBackend.getDevices()


# obtain device list (element zero) and interface list (element one)
devs, ifaces = myBackend.getDevices()
print("I've loaded the following interfaces: ")
for x in ifaces:
    print(x)
print("")
print("I've found the followin devices: ")
for n in range(0, len(devs)):
    print(f"*------------ Device n. {n:2d} ------------*")
    for key in devs[n]:
        print(f"{key:20s}: {devs[n][key]}")
    print("")


# select and connect to device
devIndex = int(input("Insert device n.> "))
print(f"Connecting to device {devIndex:d}")
myBackend.open(devs[devIndex], {"baudrate":"2000000"})


# open backend TDC
myBackend.loadModules()

# TDC
tdcModule = myBackend.getTDC()[0]
counter = myBackend.getTDCCounter()[0]




# Function to show the CT (Calibration Table):    
def show_cts(tdcModule):

	ct = []
	bin = []
	for ch_id in range(tdcModule.ch_num):
		
		tdcModule.save_calibration_data(tdcModule.CT, ch_id, "ch"+str(ch_id))
		ct_tmp = pd.read_csv(r"ch"+str(ch_id)+"_CT.csv")
		ct_tmp = ct_tmp/np.sum(ct_tmp)*(1e12*tdcModule.period)
		ct.append(ct_tmp);
		
		bin_tmp = list(range(1,len(ct_tmp)+1));
		bin.append(bin_tmp)


	fig, axs = plt.subplots(tdcModule.ch_num)
	fig.suptitle('Calibration Table')
	for ch_id in range(tdcModule.ch_num):
		axs[ch_id].plot(bin[ch_id], ct[ch_id])
		#axs[ch_id].ylabel('ps')
		#axs[ch_id].xlabel('bins')	


	
#	plt.plot(bin[0], ct[0], bin[1], ct[1], bin[2], ct[2])  
#	plt.ylabel('ps')
#	plt.xlabel('bins')
	plt.show()


# SubIntMatrix
def sub_int(x, tdcModule):
       for ch_id in range(tdcModule.ch_num):
               tdcModule.setProperty(tdcModule.SUBINTERPOLATION_MATRIX, ch_id, x)
               
	
# Valid searching (ALL CHANNELS)	
def valid_tuning(ValidNumTDL, ValidPositionTap, tdcModule):
		
	for ch_id in range(tdcModule.ch_num):
		tdcModule.setProperty(tdcModule.VALID_NUMBER_OF_TDL, ch_id, ValidNumTDL)
		tdcModule.setProperty(tdcModule.VALID_POSITION_TAP, ch_id, ValidPositionTap)
		
# Valid searching (SINGLE CHANNEL)
def valid_tuning_ch(ValidNumTDL, ValidPositionTap, tdcModule, ch_id):
        
        tdcModule.setProperty(tdcModule.VALID_NUMBER_OF_TDL, ch_id, ValidNumTDL)
        tdcModule.setProperty(tdcModule.VALID_POSITION_TAP, ch_id, ValidPositionTap)
		
		
# Set Reset internal ch	
def internal_chs(on_off, tdcModule):
		
	for ch_id in range(tdcModule.ch_num):
		tdcModule.setProperty(tdcModule.FORCECALIBRATE, ch_id, on_off)



ValidNumTDL = 0              # Change this value if you want to select another TDL to extract the valid
ValidPositionTap = 18        # Change this value if you want to select another tap (of ValidPosition_SampledTaps, see VHDL) to extract the valid
                             # Selecting higher taps will shift the CT towards right.
                             
ch = 1                       # Send this command only if you want to see the effect of the shift in a single channel


internal_chs(1, tdcModule)   
sub_int(15, tdcModule)


valid_tuning(ValidNumTDL, ValidPositionTap, tdcModule)         # Send this command to include all channels
#valid_tuning_ch(ValidNumTDL, ValidPositionTap, tdcModule, ch)  # Send this command only if you want to see the effect of the shift in a single channel 


counter.setIntegrationTime(1)
sleep(3)
print(counter.getCounts())


show_cts(tdcModule) 




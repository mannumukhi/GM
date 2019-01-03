import os
import re
from time import sleep
import sys
#iterations=sys.argv[1]
iterations=1
pass_cnt=0
fail_cnt=0
pass_cnt_map=0
fail_cnt_map=0
pass_cnt_kill=0
fail_cnt_kill=0


def GPS_ON():
        print("Enabling GPS.........")
        os.system("adb shell settings put secure location_providers_allowed +gps")

def GPS_OFF():
        print("Disabling GPS.........")
        os.system("adb shell settings put secure location_providers_allowed -gps")

def kill_map():
        print("Closing the GoogleMaps Application.......")
        os.system("adb shell am force-stop com.google.android.apps.maps")
        sleep(1)

def Validation(str2,n):
        os.system( "adb shell dumpsys activity > GPS.txt")
        with open("GPS.txt","r") as fh:
            buff=fh.readlines()
            if(n=="Launch_map"):
                if(str2 in buff):
                    return(True)
                else:
                    return(False)
            if(n=="Kill_map"):
                if(str2 not in buff):
                    return(True)
                else:
                    return(False)
        
def kill_map_validation():
        os.system("adb shell dumpsys activity > GPS.txt")
        str2=
        with open("GPS.txt","r+") as fp:
                bufr=fp.readlines()
                for line in bufr:
                        if(str2 not in line):
                                return(True)
                        else:
                                return(False)
       
def Google_map_launch():
        print("Launching the GoogleMaps Application.......")
        os.system("adb shell am start -n com.google.android.apps.maps/com.google.android.maps.MapsActivity")

def Launch_map_validation():
        os.system("adb shell dumpsys activity > GPS.txt")
        str2="packageName=com.google.android.apps.maps processName=com.google.android.apps.maps"
        with open("GPS.txt","r+") as fp:
                buffer=fp.readlines()
                for lines in buffer:
                        if(str2 in lines):
                                return(True)
                return(False)


def search_location():
        os.system("adb shell input tap 349 109")
        sleep(2)
        os.system("adb shell input text 'waverock SEZ'")
        os.system("adb shell input keyevent 66")

def sim_test():
        os.system("adb shell getprop >gsm.txt ")
        with open("gsm.txt","r+") as fh:
                lines=fh.readlines()
                for line in lines:
            #print(line)
                    string1="[gsm.sim.state]: [READY,READY]"
                    string2 = "[gsm.sim.state]: [READY,NOT_READY]"
                    string3 = "[gsm.sim.state]: [NOT_READY,READY]"
                    string4 = "[gsm.sim.state]: [ABSENT,READY]"
                    string5 = "[gsm.sim.state]: [READY,ABSENT]"
                    if (string1 in line or string2 in line or string3 in line or string4 in line or string5 in line):
                        print("Sim present, so procedding the test")
                        return 1
                else:
                        print("sim not present, please insert the sim and start the test")
                        return 0

def switch_mobiledata():
        print("Enabling the MobileData")
        os.system("adb shell svc data enable")
        sleep(3)

def mobiledata_off():
        print("Disabling the MobileData")
        os.system("adb shell svc data disable")
        sleep(1)

def validation():
        os.system("adb shell dumpsys location>text.txt")
        str1="mStarted=true"
        with open("text.txt","r") as fd:
                buf=fd.read()
                if(re.search(str1,buf,re.I)):
                        return(True)
                else:
                        return(False)
    
def checkmobiledata():
        os.system("adb shell getprop>mobiledata.txt")
        fp=open("mobiledata.txt","r+")
        buff=fp.read()
        str1="[gsm.defaultpdpcontext.active]: [true]"
        if str1 in buff:
                print(str1)
                return 1
        else:
                return 0

for i in range(int(iterations)):
        res=sim_test()
        if res:
                print("sim is present")
                switch_mobiledata()
                pre=checkmobiledata()
                if pre:
                        print("mobile data on")
                        sleep(2)
                        if(validation()):
                                print("GPS is enabled")
                                pass_cnt+=1
                                Google_map_launch()
                                if(Validation("packageName=com.google.android.apps.maps processName=com.google.android.apps.maps","Launch_map")):
                                        pass_cnt_map+=1
                                else:
                                        fail_cnt_map+=1
                                sleep(2)
                                search_location()
                                sleep(3)
                                kill_map()
                                if(Validation("packageName=com.google.android.apps.maps processName=com.google.android.apps.maps","Kill_map")):
                                        pass_cnt_kill+=1
                                else:
                                        fail_cnt_kill+=1
                else:
                        print("GPS is disabled")
                        GPS_ON()
                        sleep(2)
                        if(validation()):
                                print("GPS is enabled")
                                pass_cnt+=1
                                Google_map_launch()
                                if(Validation("packageName=com.google.android.apps.maps processName=com.google.android.apps.maps","Launch_map")):
                                        pass_cnt_map+=1
                                else:
                                        fail_cnt_map+=1
                                sleep(2)
                                search_location()
                                sleep(3)
                                kill_map()
                                if(Validation("packageName=com.google.android.apps.maps processName=com.google.android.apps.maps","Kill_map")):
                                        pass_cnt_kill+=1
                                else:
                                        fail_cnt_kill+=1
                        else:
                                fail_cnt+=1
        mobiledata_off()
print("pass_cnt=",pass_cnt)
print("fail_cnt=",fail_cnt)
print("pass_cnt_map=",pass_cnt_map)
print("fail_cnt_map=",fail_cnt_map)
print("pass_cnt_kill=",pass_cnt_kill)
print("fail_cnt_kill=",fail_cnt_kill)

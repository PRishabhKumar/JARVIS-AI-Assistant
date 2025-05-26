@echo off
echo Disconnecting old connections...
@REM adb disconnect

echo Waiting for user authorization...
adb devices
timeout 5

echo Switching to TCP/IP mode...
adb tcpip 5555
timeout 3

FOR /F "tokens=2" %%G IN ('adb shell ip addr show wlan0 ^| find "inet "') DO set ipfull=%%G
FOR /F "tokens=1 delims=/" %%G in ("%ipfull%") DO set ip=%%G

echo Connecting to device with IP %ip%...
adb connect %ip%

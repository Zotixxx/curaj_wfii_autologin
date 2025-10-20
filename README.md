# curaj_wfii_autologin
Campus Wifi Auto Installer

Description:
A simple Windows installer that installs wifi.py and simple_wifi.bat to a folder and automatically creates a scheduled task to run the script at logon with highest privileges. The script is designed to run only when connected to CAMPUS USER LOGIN Wi-Fi.

Files

CampusWifiInstaller.exe – The installer (all files are packed inside).

wifi.py – Python script (executed by .bat).

simple_wifi.bat – Batch file that runs wifi.py.

Installation

Copy CampusWifiInstaller.exe to the target PC.

Right-click → Run as Administrator.

The installer will:

Create a folder in C:\ProgramData\CampusWifi

Copy wifi.py and simple_wifi.bat there

Register a scheduled task CampusWifiAuto to run at logon

Verification

Open Task Scheduler → Task Scheduler Library

Look for task CampusWifiAuto

Trigger: At logon, Run with highest privileges

Uninstallation

Use Control Panel → Programs and Features → uninstall

Or manually remove the task:

schtasks /delete /tn CampusWifiAuto /f

Notes

Installer must be run as Administrator.

Python must be installed on the target machine (or wifi.py should be executable).

The script itself checks Wi-Fi SSID (CAMPUS USER LOGIN) before running.

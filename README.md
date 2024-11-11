# terrADBsync v1.1-beta

https://github.com/user-attachments/assets/71be4b03-1783-42b2-8817-85d478bc045a

Easy synchronization of Terraria save files between Windows/Linux/macOS and Android using ADB (Android Debug Bridge).
## Compatible with Terraria versions what?
Android Terraria v1.4.4.9.2 == PC Terraria v1.4.4.9
## What it does
- In terms of your Terraria Players and Worlds, it treats your PC and android device as one.  
- Files that are chosen to be synced are based on md5 hashing and their latest modification date.
## Concerns
- In my 90 hours of playing Terraria using this program, I have never encountered any issues.
- If Windows flags the program not recommended to run or is malicious, you can review the code.
- For further concerns, open an issue.
## Warning 
- It does not handle file conflicts. The program cannot yet take action if same files from different platforms gets modified, it ***will*** just base on the latest modified date.
> That means you can simultaneously play Terraria on your phone and PC as long as both play on different Players and Worlds.
## Bundled Features
* Backups
   - Located in the Terraria folder.
   - Has backup limitation maximum of 5 backups at a time.
* Terraria custom path support
   - Limited only to Windows and Linux
# Installation
## Android Setup
### Wired Connection
1. Enable Developer options (Locations may vary).
   - Go to Settings and find `About phone`.
   - Once there, find and press `Build number` seven times or until it notifies you that `You are now a developer!`
   - If `Build number` doesn't show up immediately, it might be in `Software information`.      
2. Plug the phone to the computer.
3. Set the Media Transfer Protocol(MTP)
   - Once plugged, there will be a notification in a form of `Use USB for`.
   - On default it is set to `Charge only`, therefore set it to `Transfer files`.
4. Enable USB debugging.
   - Back to Settings, find `Developer options`.
   - In developer options, enable `USB debugging` option located in the `DEBUGGING` section.
> It's important to note the order of step 3 and 4, otherwise, USB debugging will turn off and have to be enabled again.
> For more precise info, consider following this [guide](https://www.howtogeek.com/129728/how-to-enable-developer-options-menu-and-enable-and-usb-debugging-on-android/).
### Wireless Connection
You can also connect to your phone wirelessly when in the same local network and your phone supports it.
This method requires you to use a terminal and to have Platform Tools installed on your computer.
1. Enable Developer options (Locations may vary).
   - Go to Settings and find `About phone`.
   - Once there, find and press `Build number` seven times or until it notifies you that `You are now a developer!`.
   - If `Build number` doesn't show up immediately, it might be in `Software information`.
2. Enable USB debugging.
   - Back to Settings, find `Developer options`.
   - In developer options, enable `USB debugging` option located in the `DEBUGGING` section.
3. Enable wireless USB debugging.
   - Still in developer settings, enable and go to `Wireless debugging` just under `USB debugging` and revoke auths button.
   - Click `Pair device with pairing code` in order to see the IP address, port and a code you'll need in the next step.
4. Pair to your phone from your PC.
   - Open either your terminal or the command line.
   - Type `adb pair IP:PORT` where you replace `IP:PORT` by the address and port provided by your phone, e.g. `adb pair 192.168.1.2:45173`.
   - Type the pairing code you also got from your phone when asked `Enter pairing code:`.
## TerrADBsync Installation
In the [repository](https://github.com/Zyd8/terrADBsync/tree/main), press the green **`< > Code`** button and `Download ZIP`. Thereafter, extract it.
## PC setup and program execution
Make sure the Android Setup is finished and waiting.
### For Windows
There are two options:
 1. Run via terradbsync.exe (No manual dependency install required)

   - *Double click the terradbysnc.exe file*
       
 2. Run via terradbsync.py (requires [Python](https://www.python.org/downloads/windows/) that is [set to PATH environment](https://realpython.com/add-python-to-path/))
   - Open command-line(cmd) and change directory to *TerrADBsync-main* directory in the extracted zip file
      - `cd path/to/TerrADBsync-main`  
   - Run the `.py` file using Python (Compatible with Python versions 3.9, 3.10, or 3.11):
      - Enter `python terradbysync.py` 
      - If the above command doesn't work, try `python3 terradbsync.py`
### For Linux
 1. Run via terradbsync.py (requires [Python](https://www.python.org/downloads/linux/) that is [set to PATH environment](https://realpython.com/add-python-to-path/))
  - Launch terminal and change directory to *TerrADBsync-main* directory in the extracted zip file
      - `cd path/to/TerrADBsync-main`  
  - Run the `.py` file using Python (Compatible with Python versions 3.9, 3.10, or 3.11):
      - Enter `python terradbysync.py` or alternatively `./terradbsync.py`
      - If the above command doesn't work, try `python3 terradbsync.py`
### For macOS

> **ATTENTION: Do NOT Remove the Backups Folder!**
> 
> The macOS version of Terraria was reported corrupting the mobile saves, meaning everything is working fine up until trying to save the world on Android that was modified by your Mac. It will just hung up on 100% and do nothing.
> 
> That being said, I kindly ask you to keep track of all the changes you make to your files so you'll be able to revert everything. Hopefully, we'll find the reason and fix it.
>
> UPD 2024-11-06: The new versions (Android & macOS) of the game I tested didn't corrupt my save files this time, looks like they've fixed that.
> Still, do NOT remove the backups folder.

 1. Ensure you have Python and Platform Tools installed via [Brew](https://brew.sh):
```bash
brew install python android-platform-tools
```
 2. Run via terradbsync.py
  - Launch terminal and change directory to *TerrADBsync-main* directory in the extracted zip file
      - `cd path/to/TerrADBsync-main`  
  - Run the `.py` file using Python (Compatible with Python versions 3.9, 3.10, or 3.11):
      - Enter `./terradbsync.py` or alternatively `python3 terradbsync.py`
 # Credits
 - [Terraria](https://icons8.com/icon/52483/terraria) icon by [Icons8](https://icons8.com/)

  
 

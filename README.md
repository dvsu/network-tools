# network-tools
Basic network tools written in MicroPython for Pycom board

<br>

### Usage  
  
- Put `networktools.py` file in `lib` folder.  
- Import it from `main.py` as shown in the example below.
  
<br>

### Example  
  
```python
from networktools import Network


network = Network()

# Blocking code that will scan any known AP in the area.
# If none is found, it will retry up to 3 times
# then reset the device if still unsuccessful.
network.establishing_wlan_connection()

# Your code goes here

# To check whether or not device is connected to wireless network
# return True if device is still connected to network, else False
if network.is_connected():
    # do something
```
  
<br>
  
### Dependencies  
  
- Pycom **`WLAN`** class in **`network`** module<br><https://docs.pycom.io/firmwareapi/pycom/network/wlan/>
  
<br>
  
### Limitation  
- Type **`SSID`** and **`password`** manually in **`config.py`**<br>*(See **`config.py`** for example of data format)*
  
<br>
  
### Tested On
  
- Pycom WiPy3.0 mounted on Pycom Expansion Board 3.0
  
<br>

### Logs  

07/05/2021 
- Add **`readme`** content
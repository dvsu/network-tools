import machine
from time import sleep
from ubinascii import hexlify
from network import WLAN
from config import NETWORK_CONFIG


class Network:

    def __init__(self):
        self.wlan = WLAN(mode=WLAN.STA)
        self.found_ap = self.scanning_for_ap()
        self.known_ssid = [ap["ssid"] for ap in NETWORK_CONFIG]
        self.target_ap = {}
        self.retry = 0

    def scanning_for_ap(self) -> dict:

        ap_dict = {}

        # Scanning for AP from channel 1 to 13
        for channel_no in range(1, 14):
            ap_list = set(self.wlan.scan(channel=channel_no))

            # reconstruct the ap_list as dictionary for easy data access
            for ap in ap_list:
                ap_dict[ap.ssid] = {
                    "bssid": hexlify(ap.bssid).decode("utf-8"),
                    "sec": ap.sec,
                    "channel": ap.channel,
                    "rssi": ap.rssi
                }

        print("Detected SSID:")
        for ssid in ap_dict.keys():
            print("{}{}".format(' '*4, ssid))

        return ap_dict

    def recognized_ap_found(self) -> bool:

        found_ssid = self.found_ap.keys()

        for ssid in self.known_ssid:
            if ssid not in found_ssid:
                print("Cannot find WiFi SSID with name '{}' in the area. Rescanning...".format(ssid))
        
            else:
                self.target_ap = {
                    ssid: self.found_ap[ssid]
                }
                return True

        # If ssid is not found in known_ssid, empty the target_ap dictionary,
        # to clean old variable
        self.target_ap = {}
        
        return False

    def establishing_wlan_connection(self) -> str:

        self.retry = 0

        while True:

            try:
                if self.recognized_ap_found():
                    # If recognized_ap_found() returns True, target_ap dictionary is guaranteed to be filled,
                    # i.e. not empty. Thus "ssid" and "pwd" below will not raise error and the variable 
                    # can be safely and directly assigned

                    ssid = "".join(self.target_ap.keys())
                    pwd =  "".join([ap["pass"] for ap in NETWORK_CONFIG if ap["ssid"] == ssid])
                    
                    self.wlan.connect(ssid, auth=(self.target_ap[ssid]["sec"], pwd), timeout=5000)

                    while not self.wlan.isconnected():
                        machine.idle() # save power while waiting

                    print("Connected to WiFi SSID with name '{}'".format(ssid))

                    return ssid

                else:
                    self.retry += 1
                    self.found_ap = self.scanning_for_ap()

                # If retry for 3 times and connection is still unsuccessful, hard reset the board
                if self.retry == 3: machine.reset()

            except Exception as e:
                # This except section will handle TimeoutError potentially caused by wlan.connect()
                # when it exceeds given timeout
                print(e)
                self.retry += 1

            sleep(5)
            
    def is_connected(self) -> bool:
        return self.wlan.isconnected()

    def mac_address(self) -> str:
        return hexlify(machine.unique_id()).decode().upper()

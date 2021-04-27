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

        return False


    def establishing_wlan_connection(self) -> str:

        retry = 0

        while True:
            print("retry", retry)
            if self.recognized_ap_found():

                ssid = "".join(self.target_ap.keys())
                pwd =  "".join([ap["pass"] for ap in NETWORK_CONFIG if ap["ssid"] == ssid])
                
                self.wlan.connect(ssid, auth=(self.target_ap[ssid]["sec"], pwd), timeout=5000)

                while not self.wlan.isconnected():
                    machine.idle() # save power while waiting

                print("Connected to WiFi SSID with name '{}'".format(ssid))

                return ssid

            else:
                retry += 1
                self.found_ap = self.scanning_for_ap()

            # If retry for 3 times and connection is still unsuccessful, hard reset the board
            if retry == 3: machine.reset()

            sleep(5)
            

    def is_connected(self) -> bool:
        return self.wlan.isconnected()


    def mac_address(self) -> str:
        try:
            return hexlify(machine.unique_id()).decode().upper()

        except Exception as e:
            print("Failed to read MAC address\n{}".format(e))
            return ''

# early script to try and get all potentially non-encrypted information like passwords from captured packets

import subprocess

import pyshark

tshark_path = r'E:\Wireshark\tshark.exe'

def main():

    cap = r'C:\Users\yapla\Desktop\cap\test_cap-01.cap'

    get_hidden_ssid(cap)


    get_security_type(cap)

    #is_wpa3_downgrade_possible(cap)


    #is_wpa3_downgrade_possible(r'C:\Users\yapla\Desktop\cap\scan-01.cap')
    #for packet in capture:
    #    if 'wlan.mgt' in packet:
    #        ssid_field = packet['wlan.mgt']._all_fields.get('wlan.ssid')
    #        if ssid_field is not None:
    #            print(ssid_field.showname_value.strip('"'))

    pass

def is_wpa3_downgrade_possible(file):

    
    result = subprocess.run(
        [
            tshark_path, '-r', file,
        ]
    )

    


def get_security_type(pcap_file):
    """Print the security advertised by each access point beacon."""
    result = subprocess.run(
        [
            tshark_path, '-r', pcap_file,
            '-Y', 'wlan.fc.type_subtype == 8',
            '-T', 'fields', '-E', 'separator=|', '-E', 'occurrence=a',
            '-e', 'wlan.bssid', '-e', 'wlan.ssid',
            '-e', 'wlan.rsn.akms.type', '-e', 'wlan.wfa.ie.wpa.akms.type',
            '-e', 'wlan.fc.protected',
        ],
        capture_output=True,
        check=True,
        text=True,
    )
    seen_bssids = set()
    for line in result.stdout.splitlines():
        bssid, ssid_hex, rsn_akms, wpa_akms, protected = line.split('|')
        if not bssid or bssid in seen_bssids:
            continue
        seen_bssids.add(bssid)

        ssid = bytes.fromhex(ssid_hex).decode('utf-8', 'replace') if ssid_hex else '<hidden>'
        akms = rsn_akms or wpa_akms
        if akms:
            names = ', '.join(map_akm_type(value) for value in akms.split(','))
            protocol = 'RSN' if rsn_akms else 'WPA'
            security = f'{names}'
        elif protected == '1':
            akms = 'none'
            security = 'WEP or protected legacy network'
        else:
            akms = 'none'
            security = 'Open'

        print(f"SSID: {ssid} | BSSID: {bssid} | ({security})")

def map_akm_type(akm_val):
    """Maps the numeric AKM type to a descriptive string."""
    # Mapping based on the RSN AKM Suite definitions [citation:1][citation:4]
    akm_map = {
        '1': 'MGT',
        '2': 'PSK',
        '4': 'FT using PSK',
        '6': 'PSK (SHA256)',
        '8': 'SAE',
        '9': 'FT using SAE (SHA256)',
        '18': 'OWE',
        '24': 'SAE',
        '25': 'FT using SAE (GROUP-DEPENDENT)'
    }
    return akm_map.get(str(akm_val), 'Unknown/Other')

def get_AP_tls_cert(file):

    pass

def get_hidden_ssid(file):
    # First using the idea that someone will reconnect to the AP.
    # Using wlan.fc.type_subtype == 8  we get all the AP. Try to get the one that might be missing.
    # Then we can get things like the source address to match them.
    # ex, wlan.sa == f0:9f:c2:72:af:d2

    cap = pyshark.FileCapture(
        file,
        tshark_path=tshark_path,
        display_filter='wlan.fc.type_subtype == 8'
    )
    hidden_ssids_packets = []

    try:
        for packet in cap:
            if 'wlan.mgt' in packet:
                ssid_field = packet['wlan.mgt'].wlan_ssid
                ssid = ssid_field.showname_value.strip('"') if ssid_field is not None else None
                if ssid is not None and ssid != "" and ssid != "<MISSING>":
                    continue
                else:
                    print("Hidden SSID found in packet: ", ssid)
                    hidden_ssids_packets.append(packet)
    finally:
        cap.close()

    sa = None
    for packet in hidden_ssids_packets:
        sa = packet['wlan'].sa
        #sa = sa.showname_value.strip('"') if sa is not None else None
        print("Hidden SSID packet source address: ", sa)
        #print(packet)
        cap = pyshark.FileCapture(
                file,
                tshark_path=tshark_path,
                display_filter=f'wlan.sa == {sa}'
            )
        try:
            for packet in cap:
                if 'wlan.mgt' in packet:
                    ssid_field = packet['wlan.mgt'].wlan_ssid
                    ssid = ssid_field.showname_value.strip('"') if ssid_field is not None else None
                    if ssid is not None and ssid != "" and ssid != "<MISSING>":
                        print("Revealed SSID found in packet: ", ssid)
                    else:
                        print("Hidden SSID found in packet: ", ssid)
                        #hidden_ssids_packets.append(packet)
        finally:
            cap.close()


 



    pass



if __name__ == "__main__":
    main()


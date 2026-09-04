Simple script that is meant to help when making supplicant files.

For example, to connect to a OPN, you will need something like

//wifi-opn.conf
Network={
    ssid="<ssid>"
    key_mgmt=NONE
    scan_ssid=1
}

This project will both hold template for copy-paste and simple generator to fill all required fields.



This is a really early script and I plan to add more customization and "hand-holding" for each case.
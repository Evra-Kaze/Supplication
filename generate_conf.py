import argparse
import os



def main():
    parser = argparse.ArgumentParser(description="Generate configuration files.")

    parser.add_argument("-t", choices=["opn", "owe", "wep", "psk", "sae", "mgt"], required=True, help="Type of configuration to generate.")
    parser.add_argument("-ssid", required=True, help="SSID for the configuration.")
    parser.add_argument("-password", help="Password for the configuration (if applicable).")
    parser.add_argument("-user", help="Username for the configuration (if applicable).")
    parser.add_argument("-output", required=True, help="Output file path for the generated configuration.")

    args = parser.parse_args()

    if args.t in ["wep", "psk", "sae"] and not args.password:
        parser.error(f"Password is required for {args.t} configuration.")
    if args.t == "owe" and not args.user:
        parser.error("Username is required for OWE configuration.")

    if args.t == "opn":
        with open(args.output, "w") as f:
            f.write("Network={\n")
            f.write(f"\tSSID={args.ssid}\n")
            f.write(f"\tkey_mgmt=NONE\n")
            f.write(f"\tscan_ssid=1\n")
            f.write("}")

    if args.t == "owe":
        with open(args.output, "w") as f:
            f.write("Network={\n")
            f.write(f"\tSSID={args.ssid}\n")
            f.write(f"\tkey_mgmt=OWE\n")
            f.write("}")


    if args.t == "wep":
        with open(args.output, "w") as f:
            f.write("Network={\n")
            f.write(f"\tSSID={args.ssid}\n")
            f.write(f"\tkey_mgmt=WEP\n")
            f.write(f"\twep_key0={args.password}\n")
            f.write(f"\twep_tx_keyidx=0\n")
            f.write("}")

    if args.t == "psk":
        with open(args.output, "w") as f:
            f.write("Network={\n")
            f.write(f"\tSSID={args.ssid}\n")
            f.write(f"\tpsk={args.password}\n")
            f.write("}")

    if args.t == "sae":
        with open(args.output, "w") as f:
            f.write("Network={\n")
            f.write(f"\tSSID={args.ssid}\n")
            f.write(f"\tpsk={args.password}\n")
            f.write(f"\tkey_mgmt=SAE\n")
            f.write(f"\tieee80211w=2\n")
            f.write("}")

    if args.t == "mgt":
        with open(args.output, "w") as f:
            f.write("Network={\n")
            f.write(f"\tSSID={args.ssid}\n")
            f.write(f"\tkey_mgmt=WPA-EAP\n")
            f.write(f"\teap=PEAP\n")
            f.write(f"\tanonymous_identity=\"anonymous\"\n")
            f.write(f"\tidentity=\"{args.user}\"\n")
            f.write(f"\tpassword=\"{args.password}\"\n")
            f.write(f"\tphase2=\"auth=MSCHAPV2\"\n")
            f.write("}")










if __name__ == "__main__":
    main()
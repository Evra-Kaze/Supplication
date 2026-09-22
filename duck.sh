#!/bin/bash

# Variables
ESSID="YourSSID"
CA_DIR=~/hostapd_certs
OPENSSL_CNF=$CA_DIR/openssl.cnf
HOSTAPD_CONF=/etc/hostapd/hostapd.conf

# Create directory for certificates
mkdir -p $CA_DIR
cd $CA_DIR

# Create OpenSSL configuration file
cat > $OPENSSL_CNF <<EOL
[ ca ]
default_ca = CA_default

[ CA_default ]
dir = $CA_DIR
database = \$dir/index.txt
new_certs_dir = \$dir/newcerts
certificate = \$dir/cacert.pem
serial = \$dir/serial
private_key = \$dir/private/cakey.pem
default_days = 365
default_md = sha256
preserve = no
policy = policy_anything

[ policy_anything ]
countryName = optional
stateOrProvinceName = optional
localityName = optional
organizationName = optional
organizationalUnitName = optional
commonName = supplied
emailAddress = optional

[ req ]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = req_distinguished_name

[ req_distinguished_name ]
C = US
ST = California
L = San Francisco
O = MyCompany
OU = MyDepartment
CN = MyAP

[ v3_ca ]
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer
basicConstraints = CA:true

[ v3_req ]
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth, clientAuth
EOL

# Create necessary directories and files
mkdir -p private newcerts
chmod 700 private
touch index.txt
echo 1000 > serial

# Generate CA certificate
openssl req -new -x509 -extensions v3_ca -keyout private/cakey.pem -out cacert.pem -config $OPENSSL_CNF -days 3650

# Generate server key and certificate
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -config $OPENSSL_CNF
openssl ca -batch -keyfile private/cakey.pem -cert cacert.pem -in server.csr -out server.pem -config $OPENSSL_CNF -extensions v3_req

# Optional: Generate client key and certificate
openssl genrsa -out client.key 2048
openssl req -new -key client.key -out client.csr -config $OPENSSL_CNF
openssl ca -batch -keyfile private/cakey.pem -cert cacert.pem -in client.csr -out client.pem -config $OPENSSL_CNF -extensions v3_req

# Configure hostapd
sudo bash -c "cat > $HOSTAPD_CONF <<EOL
interface=wlan0
driver=nl80211
ssid=$ESSID
hw_mode=g
channel=6
wpa=2
wpa_key_mgmt=WPA-EAP
rsn_pairwise=CCMP

ieee8021x=1
eapol_version=2
eap_server=0
ca_cert=$CA_DIR/cacert.pem
server_cert=$CA_DIR/server.pem
private_key=$CA_DIR/server.key
EOL"

# Restart hostapd
sudo systemctl restart hostapd

echo "Certificates generated and hostapd configured successfully."
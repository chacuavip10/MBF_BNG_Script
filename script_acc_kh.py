# List các attribute
# ================QoS==================================
# Jnpr-IPv6-Ingress-Policy-Name: ipv6-U-<goi cuoc>
# Jnpr-IPv6-Egress-Policy-Name: ipv6-D-<goi-cuoc>
# Unisphere-Ingress-Policy-Name: U-VTVnet-<goi-cuoc>
# Unisphere-Egress-Policy-Name: D-VTVnet-<goi-cuoc>
# ===========Khách hàng IP dynamic - CGNAT=============
# Framed-Pool: ftth_private
# Framed-IPv6-Pool: FTTH-V6-WAN-CGNAT
# Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN-CGNAT
# Unisphere-Virtual-Router: VRF_CGNAT
# ===========Khách hàng IP dynamic - public ip=========
# Framed-IPv6-Pool: FTTH-V6-WAN
# Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN
# (Framed-Pool: default BRAS)
# ===========Khách hàng IP static======================
# Framed-Ip-Address: 137.59.42.16
# Framed-IP-Netmask: 255.255.255.255
# Framed-IPv6-Pool: FTTH-V6-WAN
# Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN
# Framed-Route: 1.1.1.1/32
# Framed-Route: 2.2.2.2/32

import ipaddress
# init
list_goi_cuoc = {1: "CN1", 2: "CN2", 3: "CN3", 4: "CN4", 5: "CN5",
                 6: "CN6", 7: "VTVnet-S30", 8: "VTVnet-S40", 9: "VTVnet-S50",
                 10: "VTVnet-S60", 11: "VTVnet-S70", 12: "VTVnet-BUSINESS-80",
                 13: "VTVnet-BUSINESS-100", 14: "VTVnet-OFFICE-120", 15: "VTVnet-OFFICE-120P",
                 16: "VTVnet-OFFICE-180", 17: "VTVnet-OFFICE-180P", 18: "VTVnet-VIP-200",
                 19: "VTVnet-VIP-200P", 20: "VTVnet-VIP-250"}
ldif = "\n"
cgnat = False
dn_start = "\ndn: uid="
dn_end = ",ou=hni,dc=mobifone,dc=vn"
common = """\nchangetype: add
objectClass: top
objectClass: person
objectClass: organizationalperson
objectClass: inetorgperson
objectClass: ftth-postpaid"""
givenname = "\ngivenname: "
sn = "\nsn: "
uid = "\nuid: "
cn = "\ncn: "
userPassword = "\n1a2b3c4d"  # Default Password
ipv4_upload = "\nUnisphere-Ingress-Policy-Name: U-"
ipv4_download = "\nUnisphere-Egress-Policy-Name: D-"
ipv6_upload = "\nJnpr-IPv6-Ingress-Policy-Name: ipv6-U-"
ipv6_download = "\nJnpr-IPv6-Egress-Policy-Name: ipv6-D-"
ipv4_static = "\nFramed-Ip-Address: "
ipv4_pool_cgnat = "\nFramed-Pool: ftth_private"
ipv6_pool = """\nFramed-IPv6-Pool: FTTH-V6-WAN
Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN"""
ipv6_pool_cgnat = """\nFramed-IPv6-Pool: FTTH-V6-WAN-CGNAT
Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN-CGNAT"""
vrf_cgnat = "\nUnisphere-Virtual-Router: VRF_CGNAT"
########Scrip main##########
username = input("Username/UID: ")
pwd = input("Password(1 to user default 1a2b3c4d): ")
if pwd == "1":
    print("Password default to: 1a2b3c4d")
else:
    userPassword = "\n" + pwd
print("===================================================")
print("Lua c")
#############
uid = uid + username


##Debug###
print(username)
print(userPassword)

print(ldif)

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
import pyperclip
import ipaddress
list_goi_cuoc = {1: "CN1", 2: "CN2", 3: "CN3", 4: "CN4", 5: "CN5",
                 6: "CN6", 7: "VTVnet-S30", 8: "VTVnet-S40", 9: "VTVnet-S50",
                 10: "VTVnet-S60", 11: "VTVnet-S70", 12: "VTVnet-BUSINESS-80",
                 13: "VTVnet-BUSINESS-100", 14: "VTVnet-OFFICE-120", 15: "VTVnet-OFFICE-120P",
                 16: "VTVnet-OFFICE-180", 17: "VTVnet-OFFICE-180P", 18: "VTVnet-VIP-200",
                 19: "VTVnet-VIP-200P", 20: "VTVnet-VIP-250"}
ldif = ""
# Init
add_user = "y"
while add_user == "y":
    # Variable for Customer type
    cgnat = False
    dynamic_sub = True
    static_ip = False
    One_block_ip = False  # neu k/h co 2 block ip, bien nay se de gia tri la True
    Two_block_ip = False
    # Variable for LDIF
    dn_start = "dn: uid="
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
    userPassword_default = "\nuserPassword: 1a2b3c4d"  # Default Password
    userPassword = "\nuserPassword: "  # Default Password
    ipv4_upload = "\nUnisphere-Ingress-Policy-Name: U-"
    ipv4_download = "\nUnisphere-Egress-Policy-Name: D-"
    ipv6_upload = "\nJnpr-IPv6-Ingress-Policy-Name: ipv6-U-"
    ipv6_download = "\nJnpr-IPv6-Egress-Policy-Name: ipv6-D-"
    ipv4_static = "\nFramed-Ip-Address: "
    ipv4_netmask = "\nFramed-Ip-Netmask: 255.255.255.255"
    ipv4_pool = ""  # ipv4_pool = "\nFramed-Pool: BRAS_01" # Them ipv4 pool neu ko su dung Pool Default
    ipv4_pool_cgnat = "\nFramed-Pool: ftth_private"
    ipv6_pool = """\nFramed-IPv6-Pool: FTTH-V6-WAN
Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN"""
    ipv6_pool_cgnat = """\nFramed-IPv6-Pool: FTTH-V6-WAN-CGNAT
Jnpr-IPv6-Delegated-Pool-Name: FTTH-V6-LAN-CGNAT"""
    vrf_cgnat = "\nUnisphere-Virtual-Router: VRF_CGNAT"
    sub_ipv4_static_input = ""
    ########Scrip main##########
    username = input("(Input) Username/UID: ")
    pwd = input("(Input) Password (Enter \"1\" to use default: \"1a2b3c4d\"): ")
    if pwd == "1":
        userPassword = userPassword_default
        print("==>(Info) Password default to: 1a2b3c4d")
    else:
        userPassword += pwd
    # goi cuoc
    print("===================================================")
    print("**                 List goi cuoc                 **")
    print("===================================================")
    for x in list_goi_cuoc:
        print(f"{x}: {list_goi_cuoc[x]}")
    print("===================================================")
    id = 100
    while (int(id) >= 21) or (int(id) <= 0):  # change condition neu them goi cuoc
        plan_id = input("(Input) ID goi cuoc? (1-20): ")
        id = plan_id
    # Lay ten goi cuoc dua theo ID tu list_goi_cuoc
    plan = list_goi_cuoc.get(int(plan_id))
    print(f"==>(Info) Goi cuoc: {plan}")
    #######################################################################################################
    #### *************Neu them goi cuoc, thay doi doan code nay cho phu hop***************************####
    if 1 <= int(plan_id) <= 6:
        cgnat = True
        dynamic_sub = True
        static_ip = False
        One_block_ip = False
        Two_block_ip = False
    elif 7 <= int(plan_id) <= 11:
        cgnat = False
        dynamic_sub = True
        static_ip = False
        One_block_ip = False
        Two_block_ip = False
    elif 12 <= int(plan_id) <= 17:
        cgnat = False
        dynamic_sub = False
        static_ip = True
        One_block_ip = False
        Two_block_ip = False
    elif 18 <= int(plan_id) <= 19:
        cgnat = False
        dynamic_sub = False
        static_ip = True
        One_block_ip = True
        Two_block_ip = False
    elif int(plan_id) == 20:
        cgnat = False
        dynamic_sub = False
        static_ip = True
        One_block_ip = True
        Two_block_ip = True
    #############################################################
    # Input k/h ip tinh (public ip)
    if static_ip:  # equal static_ip == True
        print("==>(Info) Goi cuoc bao gom 01 ip tinh!")
        loop = True
        while loop == True:
            try:
                IP_Static = input("(Input) Dia chi Ip tinh: ")
                if ipaddress.ip_address(IP_Static).is_private == True:
                    loop = True
                    print(
                        "==> (Error) Dia chi ip la private, moi nhap lai dia chi public!")
                else:
                    loop = False
            except ValueError:
                print("==> (Error) Sai cu phap dia chi ip! (x.x.x.x, x <= 255)")
        sub_ipv4_static_input = ipv4_static + \
            IP_Static + ipv4_netmask  # Update ip static
    # Info
    if One_block_ip & Two_block_ip:  # One_block_ip = Two_block_ip = True
        print("==>(Info) Goi cuoc bao gom 02 block ip tinh!")
    elif (One_block_ip == True) & (Two_block_ip == False):
        print("==>(Info) Goi cuoc bao gom 01 block ip tinh!")
    # Input block ip 1
    if One_block_ip | Two_block_ip:  # One_block_ip = True or Two_block_ip = True
        loop = True
        while loop == True:
            try:
                Framed_Route_1 = ipaddress.ip_network(
                    input("(Input) Block IP , subnetmask default /32: "))
                if ipaddress.ip_network(Framed_Route_1).is_private == True:
                    loop = True
                    print(
                        "==> (Error) Dai dia chi ip la private, moi nhap lai dai dia chi public!")
                else:
                    loop = False
            except ValueError:
                print("==> (Error) Sai cu phap block ip! (ipaddress/subnetmask)")
        sub_ipv4_static_input = sub_ipv4_static_input + \
            "\nFramed-Route: " + str(Framed_Route_1)
    # Input block ip 2
    if Two_block_ip:  # change condition neu them goi cuoc
        loop = True
        while loop == True:
            try:
                Framed_Route_2 = ipaddress.ip_network(
                    input("(Input) Block IP 2, subnetmask default /32: "))
                if ipaddress.ip_network(Framed_Route_2).is_private == True:
                    loop = True
                    print(
                        "==> (Error) Dai dia chi ip la private, moi nhap lai dai dia chi public!")
                else:
                    loop = False
            except ValueError:
                print("==> (Error) Sai cu phap block ip! (ipaddress/subnetmask)")
        sub_ipv4_static_input = sub_ipv4_static_input + \
            "\nFramed-Route: " + str(Framed_Route_2)
    # Print block ip
    if (One_block_ip == True) & (Two_block_ip == False):
        print(f"==>(Info) Block IP: {Framed_Route_1}")
    elif Two_block_ip:
        print(f"==>(Info) Block IP: {Framed_Route_1} {Framed_Route_2}")
    # Generate LDIF file
    # 0. Update variable
    givenname += username
    sn += username
    uid += username
    cn += username

    ipv4_upload += plan
    ipv4_download += plan
    ipv6_upload += plan
    ipv6_download += plan
    # 1. add dn, uid
    if cgnat:  # update neu update list goi cuoc
        ldif = ldif + dn_start + username + ",cn=" + plan + dn_end
    else:
        ldif = ldif + dn_start + username + dn_end
    # 2. add common
    ldif = ldif + common
    # 3. add account info
    ldif = ldif + givenname + sn + uid + cn + userPassword
    # 4. add policy upload/download ipv4, ipv6
    ldif = ldif + ipv4_download + ipv4_upload + ipv6_download + ipv6_upload
    # 5. cho k/h CGNAT ==> End of Ldif
    # print(f"cgnat: {cgnat}, dynamic_sub: {dynamic_sub}")
    if (cgnat == True) & (dynamic_sub == True):
        ldif = ldif + ipv4_pool_cgnat + ipv6_pool_cgnat + vrf_cgnat
    if (cgnat == False) & (dynamic_sub == True):
        ldif = ldif + ipv4_pool + ipv6_pool
    # 6. cho k/h ip tinh, no block ip
    ldif = ldif + sub_ipv4_static_input
    ldif += "\n\n"
    print(f"==>(Info) Add user <{username}> to ldif file!")
    add_user = input(
        "\n==>(Input) Them khach hang? (choose y for yes, any other keys for no): ")
##Debug###
# print(sub_ipv4_static_input)

##########################LDIF OUTPUT#########################################################
ldif = ldif.rstrip()
ldif = ldif.lstrip()
print("================================================================================\n")
print(""" .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. |
| |   _____      | || |  ________    | || |     _____    | || |  _________   | |
| |  |_   _|     | || | |_   ___ `.  | || |    |_   _|   | || | |_   ___  |  | |
| |    | |       | || |   | |   `. \ | || |      | |     | || |   | |_  \_|  | |
| |    | |   _   | || |   | |    | | | || |      | |     | || |   |  _|      | |
| |   _| |__/ |  | || |  _| |___.' / | || |     _| |_    | || |  _| |_       | |
| |  |________|  | || | |________.'  | || |    |_____|   | || | |_____|      | |
| |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------' """)
print("================================================================================\n")
print(ldif)
print("\n============================================")
# Write to file
pyperclip.copy(ldif)
f = open("add_new_user.ldif", "w")
f.write(ldif)
f.close()
input("Write to Clipboard & add_new_user.ldif!, press any key to quit!")

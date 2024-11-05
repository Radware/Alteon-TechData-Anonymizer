import re
import os
import tarfile
import time
from datetime import datetime
from tkinter.filedialog import askopenfilename
import traceback
from pathlib import Path
import random
import sys

try:
    list_of_patterns_to_Anonymized = [
        "applog",
        "/disk/logs",
        "tsdmp",
        "panicdumps",
        "/disk/Alteon/logs",
        "/disk/Alteon/Config/",
        "/logs/syslog",
        "/logs/console_logs"
        # "config_vx.txt"
    ]

    list_of_patterns_to_not_Anonymize = [
        "/disk/Alteon/Config/dassh",
        ".tgz",
        ".cap",
        ".pcap",
        "vantage"
    ]

    list_of_config_files = [
        "config_vx.txt",
        "config1.txt",
        "config2.txt"
    ]

    random_1 = random.randint(10, 100)
    random_2 = random.randint(10, 100)
    random_3 = random.randint(10, 100)
    random_4 = random.randint(10, 100)
    #
    #
    #
    # print("Random-1 is", random_1)
    # print("Random-2 is", random_2)
    # print("Random-3 is", random_3)
    # print("Random-4 is", random_4)
    #
    random_list = random_1, random_2, random_3, random_4


    def generate_IP(IP):
        #print(IP)
        str_IP = str(IP)
        if str_IP.startswith("255."):
            return str_IP

        IP_octets = str_IP.split(".")

        count = 0
        new_IP = ''
        for octet in IP_octets:
            #print(octet)
            octet = int(octet)
            if octet <= 128 and count < 3:
                octet += random_list[count]
            # elif count == 3 and octet == 255:
            #     pass
            elif octet > 128 and count < 3:
                octet -= random_list[count]

            #print(octet)
            if count < 3:
                new_IP += str(octet) + '.'
            elif count == 3:
                new_IP += str(octet)
            count += 1

        #print(new_IP)
        return new_IP

    list_of_words_to_remove = []
    current_path = os.path.abspath(os.getcwd())

    # print("Current PATH:", current_path)

    with open(current_path + r"\custom_words_to_remove.txt") as file:
        print("Custom words to remove:")
        for line in file:
            for word in line.split():
                print(word)
                list_of_words_to_remove.append(word)

    print('')
    print("Please choose the TechData File:")
    filename = askopenfilename()
    print("File is:", filename, "\n")

    anonymize_or_random = input('Choose "1" To anonymize also the IP addresses in the config files (IP.IP.IP.IP will be x.x.x.x)\n'
                            'Choose "2" To randomize the IP addresses in the config files (IP.IP.IP.IP will be RANDOM.RANDOM.RANDOM.IP)\n'
                            'Please type your choice:')
    print("Client input is -->", anonymize_or_random)
    if anonymize_or_random != "1" and anonymize_or_random != "2":
        print('Invalid input, the input should be "1" or "2".')
        time.sleep(2)
        sys.exit()


    now = datetime.now()
    print("now =", now)

    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    print("date and time =", dt_string)

    pattern = re.compile(r"(?<!Version )(?<!Version: )\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b")
    public_cert = re.compile(r"(?<=-----BEGIN CERTIFICATE-----).*?(?=-----END CERTIFICATE-----)", flags=re.DOTALL)
    csr = re.compile(r"(?<=-----BEGIN CERTIFICATE REQUEST-----).*?(?=-----END CERTIFICATE REQUEST-----)",
                     flags=re.DOTALL)
    cert_private_key = re.compile(r"(?<=-----BEGIN RSA PRIVATE KEY-----).*?(?=-----END RSA PRIVATE KEY-----)",
                                  flags=re.DOTALL)

    usr_adm_pw = re.compile(r"(?<=usrpw |admpw ).*?(?=$)", flags=re.MULTILINE)

    pswd = re.compile(r"(?<=pswd ).*?(?=$)", flags=re.MULTILINE)
    passphrase = re.compile(r"(?<=/c/slb/sync/passphrs ).*?(?=$)", flags=re.MULTILINE)
    auth = re.compile(r"(?<=auth ).*?(?=$)", flags=re.MULTILINE)
    esecret = re.compile(r"(?<=esecret ).*?(?=$)", flags=re.MULTILINE)
    token = re.compile(r"(?<=token=).*?(?=$)", flags=re.MULTILINE)
    basic_authentication = re.compile(r"(?<=Authorization: Basic ).*?(?=$)", flags=re.MULTILINE)
    tag = re.compile(r"(?<=tag ).*?(?=$)", flags=re.MULTILINE)
    taglist = re.compile(r"(?<=taglist ).*?(?=$)", flags=re.MULTILINE)
    index = re.compile(r"(?<=index ).*?(?=$)", flags=re.MULTILINE)
    name = re.compile(r"(?<=name ).*?(?=$)", flags=re.MULTILINE)
    uname = re.compile(r"(?<=uname ).*?(?=$)", flags=re.MULTILINE)
    SNMP_rcomm_wcomm = re.compile(r"(?<=rcomm |wcomm ).*?(?=$)", flags=re.MULTILINE)

    home = str(Path.home())
    print(home)

    # anonymized_path = home + r'\Desktop\anonymized_from_' + dt_string
    anonymized_path = current_path + r'\anonymized_from_' + dt_string
    os.makedirs(anonymized_path)

    tar = tarfile.open(filename, "r:gz")
    for member in tar.getmembers():
        print(member.name)
        # print(type(member.name))

        counter = 0
        for i in list_of_patterns_to_Anonymized:
            if i in member.name:
                counter = 1
                break

        for i in list_of_patterns_to_not_Anonymize:
            if i in member.name:
                counter = 0
                break



        if counter == 1:

            folder_name = os.path.dirname(member.name)
            # print("Folder is -->", folder_name)
            if not os.path.exists(anonymized_path + folder_name):
                os.makedirs(anonymized_path + folder_name)
            try:
                f = tar.extractfile(member)
            except KeyError as error:
                print(error)
                print(member.name, "is not found")
                continue
            # print(f)
            if f is not None:
                content = f.read()
                # print(type(content))
                # content_str = content.decode("ascii", errors='ignore')
                content_str = content.decode("ascii", errors='ignore')
                # print(type(content_str))
                # print(content_str)
                print("Start anonymizing ---->", member.name)
                # replaced = re.sub(pattern, 'x.x.x.x', content_str)


                if anonymize_or_random == "2": # which means randomize the IP addresses in the config file
                    flag = 0
                    for i in list_of_config_files:
                        if i in member.name:
                            flag = 1
                            break

                    if flag == 1:

                        all_IPs = re.findall(pattern, content_str)
                        #print(all_IPs)
                        for IP in all_IPs:
                            new_IP = generate_IP(IP)
                            #print(IP)
                            #print(new_IP)
                            #str_IP = str(IP)
                            content_str = content_str.replace(IP, new_IP, 1)
                        replaced = content_str
                    else:
                        replaced = re.sub(pattern, 'x.x.x.x', content_str)
                else: # which means anonymize also the config file with x.x.x.x instead of IP
                    replaced = re.sub(pattern, 'x.x.x.x', content_str)


                replaced = re.sub(public_cert, '\nXXXXX PUBLIC-CERT XXXXX\n', replaced)
                replaced = re.sub(csr, '\nXXXXX CSR XXXXX\n', replaced)
                replaced = re.sub(cert_private_key, '\nXXXXX KEY XXXXX\n', replaced)

                replaced = re.sub(usr_adm_pw, '"XXXXX"', replaced)
                replaced = re.sub(pswd, '"XXXXX"', replaced)
                replaced = re.sub(passphrase, 'XXXXX', replaced)
                replaced = re.sub(auth, 'XXXXX', replaced)
                replaced = re.sub(esecret, 'XXXXX', replaced)
                replaced = re.sub(token, 'XXXXX', replaced)
                replaced = re.sub(basic_authentication, 'XXXXX', replaced)
                replaced = re.sub(tag, 'XXXXX', replaced)
                replaced = re.sub(taglist, 'XXXXX', replaced)
                replaced = re.sub(index, 'XXXXX', replaced)
                replaced = re.sub(name, 'XXXXX', replaced)
                replaced = re.sub(uname, 'XXXXX', replaced)
                replaced = re.sub(SNMP_rcomm_wcomm, 'XXXXX', replaced)


                for word_to_remove in list_of_words_to_remove:
                    replaced = re.sub(word_to_remove, 'XXXXXXXXXX', replaced, flags=re.I)
                # print(replaced)
                # print(type(replaced))

                filePath = anonymized_path + member.name
                new_file = open(filePath, "w")
                new_file.write(replaced)
                new_file.close()
                print(member.name, "has been successfully anonymized\n")
        else:
            print("Skipping\n")
            pass

except Exception as error:
    print(error)
    print(traceback.format_exc())

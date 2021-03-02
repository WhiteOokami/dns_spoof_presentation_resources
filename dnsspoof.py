import socket
import multiprocessing
import subprocess
import os
import threading

targets = []
HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "disconnected"

def pinger(job_q, results_q):
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass

def findDevices(myIp):
    #find targets near your  (parts of this was removed)
    SERVER = socket.gethostbyname(myIp)
    print(SERVER)
    ADDR = (SERVER, PORT)
    print(myIp)

    ip_list = list()

    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()
    pool_size=255
    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    for i in range(1, 255):
        jobs.put(myIp + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    while not results.empty():
        ip = results.get()
        ip_list.append(ip)


def poisonCache(targetIp):
    #poison the DNS cache
    a = 1
    print("TARGETS:")
    for i in targets:
        print(str(a)+'. '+i)
    print("removed for your safety") #no illegal activities lmao

def youNeedSomeHelp():
    print("[This program is garbage, I removed a bunch of the code so you won't get in trouble ;) ]")
    print("STEPS:")
    print("1. find nearby targets using the command: -f YOUR_IP (use ifconfig to get ip)")
    print("2. add targets: -t TARGET_IP (for each target)")
    print("3. use apache to host your website: (use git or apt-install to download)")
    print("4. run the dns spoof: -r")
    print("(the spoofing is happening on port 5050)")
    print("(this program prob only works in Linux) \n")

def addTarget(target):
    targets.append(target)
    print("ADDED: "+target)
a = '-'
try:
    while a != 'q':
        print("Haha, type something (-h for help):")
        a = input()
        if (a == '-h'):
            youNeedSomeHelp()

        if (a.split()[0] == '-f'):
            ip = a.split()[1]
            findDevices(ip)

        if (a.split()[0] == '-t'):
            addTarget(a.split()[1])

        if (a.split()[0] == '-r'):
            poisonCache(targets)
except:
    print("uhh, error (check if you have enough parameters)")
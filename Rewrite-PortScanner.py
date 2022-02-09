import socket
import queue
import threading
import argparse
import sys

que = queue.Queue() #初始化一个队列，用于保存扫描端口队列

class PortScanner(threading.Thread):
    def __init__(self, host):
        super().__init__()
        self.host = str(host)

    def run(self) -> None:
        while 1:
            port = que.get()
            self.scanner(port)
            que.task_done()

    def scanner(self, port):
        conn = socket.socket()
        try:
            conn.connect((self.host, port))
            print(f'[+]Port{port}:Open.')
        except:
            pass

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description='PortScanner by socket', exit_on_error=False)
        parser.add_argument('-host', required=True)
        parser.add_argument('-sPort', required=True)
        parser.add_argument('-ePort', required=True)
        parser.add_argument('-thnum', required=False)
        args = parser.parse_args()
        if args.thnum == None:
            threadnumber = 500
            print('[*]Default Threadnumber is 500.')
        else:
            threadnumber = args.thnum
            print('[*]Threadnumber is %s.' %(args.thnum))
    except:
        print("[-]usage:python PortScanner.py -host 'domainName or IP address' -sPort 'startport' -ePort 'endport' -thnum 'anynumber' ")
        sys.exit(0)
    ip = socket.gethostbyname(args.host)
    
    for i in range(int(threadnumber)):
        t = PortScanner(ip)
        t.setDaemon(1) #添加守护进程
        t.start()

    for i in range(int(args.sPort), int(args.ePort)+1): #根据第二第三项输入构建队列，左闭右开区间，所以endport+1
        que.put(i)

    que.join()
    print('[+]Scan Done.')
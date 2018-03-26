from socket import *
from optparse import OptionParser
from threading import Thread, Semaphore


_lock = Semaphore(value=1)
def connection_scan(host, port):
    """
    From given tuple host:port, try to connect to it
    """
    con = socket(AF_INET, SOCK_STREAM)
    try:
        con.connect((host, port))
        con.send('DummyText\r\n')
        results = con.recv(100)
        _lock.acquire()
        print("[+] {}:{} TCP Connection Open!".format(host, port))
        print("[+] {}!".format(results))
    except Exception, e:
        _lock.acquire()
        print("[-] {}:{} TCP Connection Closed because {}!".format(host, port, e))
    finally:
        _lock.release()
        con.close()


def port_scan(host, ports, threading=False):
    """
    From given list of ports, try connecting given host to each port
    """
    try:
        host_ip = gethostbyname(host)
    except:
        print("[-] Cannot resolve host \"{}\". Unknown host.".format(host))
        return

    try:
        host_name = gethostbyaddr(host_ip)
        print("[+] Scan Results for: {}".format(host_name[0]))
    except:
        print("[+] Scan Results for: {}".format(host_ip))

    setdefaulttimeout(1)
    for port in ports:
        print("[.] Scanning host {}:{}".format(host, port))
        if threading:
            t = Thread(target=connection_scan, args=(host, port))
            t.start()
        else:
            connection_scan(host, port)





if __name__ == "__main__":
    parser = OptionParser('usage %prog -H <target host> -p <target_port(s)>')
    parser.add_option('-H', dest='target_host', type=str, help='Specify target host.')
    parser.add_option('-p', dest='target_ports', type=str, help='Specify target port(s) separated by comma.')
    parser.add_option('-t', dest='threading', action="store_true", help='Allow threading when connecting to different hosts.')

    (options, args) = parser.parse_args()

    if options.target_host is None or options.target_ports is None:
        print(parser.usage)
        exit(0)

    # Split string "<port1>, <port2>, " into list of ints [<port1>, <port2>]
    target_ports = map(int, filter(None, map(lambda p: p.strip(), options.target_ports.split(","))))
    port_scan(options.target_host, target_ports, options.threading)

    print(options)
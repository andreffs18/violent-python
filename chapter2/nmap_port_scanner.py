import nmap
from optparse import OptionParser


def nmap_scan(host, port):
    """
    Scan host and port with library Nmap
    """
    nmScan = nmap.PortScanner()
    nmScan.scan(host, port)
    if nmScan.scaninfo().get('error'):
        print("[-] {} tcp/{} -> {}".format(host, port, nmScan.scaninfo().get('error')))
        return

    result = nmScan._scan_result
    for _ip in result['scan'].keys():
        state = result['scan'][_ip]['tcp'][int(port)]['state']
        print("[+] {} tcp/{} {}".format(host, port, state))



if __name__ == "__main__":
    parser = OptionParser('usage %prog -H <target host> -p <target_port(s)>')
    parser.add_option('-H', dest='target_host', type=str, help='Specify target host.')
    parser.add_option('-p', dest='target_ports', type=str, help='Specify target port(s) separated by comma.')

    (options, args) = parser.parse_args()

    if options.target_host is None or options.target_ports is None:
        print(parser.usage)
        exit(0)

    # Split string "<port1>, <port2>, " into list of string [<port1>, <port2>]
    target_ports = filter(None, map(lambda p: p.strip(), options.target_ports.split(",")))
    for port in target_ports:
        nmap_scan(options.target_host, port)

    print(options)
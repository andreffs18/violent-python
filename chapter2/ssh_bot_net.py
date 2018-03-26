from pexpect import pxssh

PROMPT = ["# ", ">>> ", "> ", "$ "]


def connect(host, user, password):
    """
    Return SSH connection for given username@host -p password
    """
    s = pxssh.pxssh()
    try:
        s.login(host, user, password)
    except:
        print("[-] Error connecting.")
        exit(0)

    return s


def send_command(s, cmd):
    """
    Execute given "cmd" onto open child ssh connection
    """
    s.sendline(cmd)
    s.prompt()
    print(s.before)


if __name__ == "__main__":
    child = connect("localhost", "root", "toor")
    if not child:
        exit(0)
    send_command(child, 'cat /etc/shadow | grep root')



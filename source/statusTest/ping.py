import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import os

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0



def ping2(host):
    response = os.system("ping -c 1 " + host)

    #and then check the response...
    if response == 0:
        print(host, 'is up!')
    else:
        print(host, 'is down!')

if __name__ == "__main__":
    host = 'https://uvb1bb4153.execute-api.eu-central-1.amazonaws.com'
    host = 'google.com'
    ping2(host)

    


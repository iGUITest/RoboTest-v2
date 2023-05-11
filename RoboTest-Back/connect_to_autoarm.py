"""
Used to set the parameters of the connected robot arm
"""
import paramiko


def connect():
    host_ip = '192.168.101.10'
    username = 'ubuntu'
    password = 'hiwonder'
    try:
        t = paramiko.Transport((host_ip, 22))
        t.connect(username=username, password=password)
        return t
    except:
        return None

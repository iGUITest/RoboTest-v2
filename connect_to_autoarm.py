"""
用于设置连接机械臂的参数
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

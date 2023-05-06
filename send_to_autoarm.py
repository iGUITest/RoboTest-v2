"""
用于向机械臂发送文件
"""
import paramiko
from connect_to_autoarm import connect


def send_to_autoarm(file_path, file_name):
    t = connect()
    if t is not None:
        sftp = paramiko.SFTPClient.from_transport(t)
        src = file_path
        des = '/home/ubuntu/TestRobot/temp/' + file_name
        sftp.put(src, des)
        t.close()
    else:
        return False

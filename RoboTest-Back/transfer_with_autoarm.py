"""
Used to send and receive files with the robotic arm
"""
import paramiko
from connect_to_autoarm import connect


def send_to_autoarm(src, des):
    t = connect()
    if t is not None:
        try:
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.put(src, des)
            t.close()
            return True
        except:
            return False
    else:
        return False


def get_from_autoarm(src, des):
    t = connect()
    if t is not None:
        try:
            sftp = paramiko.SFTPClient.from_transport(t)
            sftp.get(src, des)
            t.close()
            return True
        except:
            return False
    else:
        return False

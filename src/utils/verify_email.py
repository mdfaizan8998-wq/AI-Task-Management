from email.message import EmailMessage
import smtplib
import socket

# IPv4 Fix ko function ke bahar ek hi baar run karein
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [r for r in responses if r[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

def send_email(receiver_email: str, otp: str):
    msg = EmailMessage()
    msg["Subject"] = "Verify Your Email - Todo App"
    msg["From"] = "md.faizan8998@gmail.com"
    msg["To"] = receiver_email

    msg.set_content(f"""
Welcome to Todo App!

Your email verification OTP is: {otp}

This OTP is valid for 10 minutes.

Do not share this OTP with anyone.

Regards,
Todo App Team
""")

    try:
        print(f"🔄 [Background] Attempting to send email to {receiver_email}...")
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as smtp:
            smtp.starttls() 
            smtp.login("md.faizan8998@gmail.com", "scyr beod baif ukif")
            smtp.send_message(msg)
            print(f"✅ Email sent successfully to {receiver_email}!")
            return True
    except Exception as e:
        print(f"💥 EMAIL ERROR: {e}")
        print(f"🔑 BYPASS OTP FOR TESTING: User {receiver_email} ka OTP hai: {otp}")
        return False

from email.message import EmailMessage
import smtplib
import socket

# IPv4 Force karne ka zyada safe aur clean tarika
# Isme kwargs ka jhanjhat nahi hota aur smtplib crash nahi karega
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    # Family ko strictly socket.AF_INET (IPv4) par force kar rahe hain
    return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
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
        
        # Timeout ko thoda badha diya hai (15s) taaki slow network pe fail na ho
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as smtp:
            smtp.ehlo()      # Server ko greet karne ke liye (Good practice)
            smtp.starttls()  # Connection encrypt karne ke liye
            smtp.ehlo()      # TLS ke baad fir se greet karein
            
            # NOTE: Password se spaces hata diye hain ("scyrbeodbaifukif")
            smtp.login("md.faizan8998@gmail.com", "scyrbeodbaifukif")
            
            smtp.send_message(msg)
            print(f"✅ Email sent successfully to {receiver_email}!")
            return True
            
    except Exception as e:
        print(f"💥 EMAIL ERROR: {type(e).__name__} - {e}")
        print(f"🔑 BYPASS OTP FOR TESTING: User {receiver_email} ka OTP hai: {otp}")
        return False

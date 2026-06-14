
from email.message import EmailMessage
import smtplib

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
    

   with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as smtp:
        smtp.starttls()
            "md.faizan8998@gmail.com",
            "scyr beod baif ukif"
        )
        smtp.send_message(msg)


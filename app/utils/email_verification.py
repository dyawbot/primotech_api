import smtplib
from email.message import EmailMessage
import os
from app.core.config import settings

def send_verification_email(toEmail, token) -> bool:
    try:
        verification_link =  f"{settings.API_URL}/me?id={token}"
        msg = EmailMessage()
        msg["Subject"] = "Verify Account"
        msg["From"] = settings.ADMIN_EMAIL
        msg["To"] = toEmail
        # msg.set_content(f"Click here to verify your email: {verification_link}")
        msg.set_content(
            f"Hello,\n\nPlease verify your email by clicking the link below:\n{verification_link}\n\n"
            "If you did not request this, please ignore this email.\n\n"
            "Thank you."
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(settings.ADMIN_EMAIL, settings.ADMIN_PASS)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print("\n\n\n")
        print(e)
        return False



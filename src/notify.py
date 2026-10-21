"""Email notification helpers for OrderSystem."""

import os
import smtplib
import ssl
from email.mime.text import MIMEText

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
SMTP_TIMEOUT = float(os.getenv("SMTP_TIMEOUT", "10"))


def send_email(to, subj, body):
    """Send an email using STARTTLS; return False if SMTP delivery fails."""
    if not to:
        return False

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subj
    msg["From"] = SMTP_USER
    msg["To"] = to

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=SMTP_TIMEOUT) as server:
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            if SMTP_USER:
                server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True
    except (smtplib.SMTPException, OSError, ValueError):
        return False


def notify_user(user_id, msg_type, data=None):
    """Send the email associated with a supported notification type."""
    data = data or {}
    email = data.get("email", "")
    if msg_type == 1:
        return send_email(
            email,
            "Order Confirmed",
            "Your order #{} has been confirmed.".format(data.get("order_id")),
        )
    if msg_type == 2:
        return send_email(
            email,
            "Payment Received",
            "Payment of {} UAH received.".format(data.get("amount")),
        )
    if msg_type == 3:
        return send_email(
            email,
            "Order Cancelled",
            "Your order #{} was cancelled.".format(data.get("order_id")),
        )
    return False


def bulk_notify(users, msg):
    """Send a message to each user and return sent/failed counts."""
    sent = 0
    failed = 0
    for user in users:
        try:
            if send_email(user.get("email", ""), "Notification", msg):
                sent += 1
            else:
                failed += 1
        except Exception:
            failed += 1
    return {"sent": sent, "failed": failed}


def log_notification(user_id, tp, status):
    """Placeholder for persistent notification logging."""
    return None

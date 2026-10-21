"""Tests for the CR-011 SMTP notification fix."""

from unittest.mock import MagicMock, patch

from src import notify


@patch("src.notify.smtplib.SMTP")
def test_send_email_uses_starttls_and_sends_message(mock_smtp):
    server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = server

    with patch.object(notify, "SMTP_USER", "sender@example.com"), patch.object(
        notify, "SMTP_PASS", "secret"
    ), patch.object(notify, "SMTP_HOST", "smtp.example.com"), patch.object(
        notify, "SMTP_PORT", 587
    ):
        result = notify.send_email("customer@example.com", "Subject", "Body")

    assert result is True
    mock_smtp.assert_called_once()
    server.starttls.assert_called_once()
    server.login.assert_called_once_with("sender@example.com", "secret")
    server.send_message.assert_called_once()
    message = server.send_message.call_args.args[0]
    assert message["To"] == "customer@example.com"
    assert message["Subject"] == "Subject"


@patch("src.notify.smtplib.SMTP")
def test_send_email_returns_false_when_smtp_fails(mock_smtp):
    mock_smtp.side_effect = notify.smtplib.SMTPException("connection failed")
    assert notify.send_email("customer@example.com", "Subject", "Body") is False


def test_send_email_returns_false_for_empty_recipient():
    assert notify.send_email("", "Subject", "Body") is False


@patch("src.notify.send_email", return_value=True)
def test_notify_user_sends_order_confirmation(mock_send_email):
    result = notify.notify_user(
        7, 1, {"email": "customer@example.com", "order_id": 42}
    )
    assert result is True
    mock_send_email.assert_called_once_with(
        "customer@example.com",
        "Order Confirmed",
        "Your order #42 has been confirmed.",
    )


@patch("src.notify.send_email", return_value=False)
def test_notify_user_propagates_delivery_failure(mock_send_email):
    result = notify.notify_user(7, 1, {"email": "customer@example.com", "order_id": 42})
    assert result is False


@patch("src.notify.send_email", return_value=True)
def test_bulk_notify_counts_failures(mock_send_email):
    mock_send_email.side_effect = [True, False]
    result = notify.bulk_notify(
        [{"email": "one@example.com"}, {"email": "two@example.com"}], "Hello"
    )
    assert result == {"sent": 1, "failed": 1}

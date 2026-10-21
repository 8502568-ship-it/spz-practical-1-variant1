# Changelog

## 2026-10-21 — CR-011: SMTP notification delivery

- Replaced the email-notification stub with SMTP delivery using STARTTLS and a verified SSL context.
- Moved SMTP host, port, credentials, and timeout to environment variables.
- Added explicit success/failure results and error handling for SMTP delivery.
- Added mocked SMTP tests for delivery, error handling, empty recipients, order confirmation, and bulk result counts.
- Validation in GitHub Actions: 15 tests passed; total `src/` coverage 43%; `src/notify.py` coverage 84%; Pylint 10.00/10.
- Real SMTP delivery still requires staging credentials and a controlled test recipient.

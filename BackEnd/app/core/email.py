import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_verification_email(to_email: str, code: str) -> None:
    """
    Təsdiqləmə kodunu email ilə göndərir.
    SMTP tənzimlənməyibsə (inkişaf mərhələsində), kodu sadəcə konsola çap edir —
    beləcə hələ email quraşdırmamış olsanız belə, kodu logs-dan görə bilərsiniz.
    """
    if not settings.smtp_username or not settings.smtp_password:
        print(f"[DEV] {to_email} üçün təsdiqləmə kodu: {code}")
        return

    from_email = settings.smtp_from_email or settings.smtp_username

    message = MIMEMultipart("alternative")
    message["Subject"] = "Qarabağ Tur Platforması — Email təsdiqləmə kodu"
    message["From"] = from_email
    message["To"] = to_email

    text_body = f"Salam!\n\nEmail təsdiqləmə kodunuz: {code}\n\nBu kod 15 dəqiqə ərzində etibarlıdır."
    html_body = f"""
    <div style="font-family: Arial, sans-serif; padding: 24px; max-width: 480px; margin: 0 auto;">
      <h2 style="color: #2e7d32;">Email təsdiqləmə</h2>
      <p>Qeydiyyatınızı tamamlamaq üçün aşağıdakı kodu tətbiqdə daxil edin:</p>
      <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #1b1b1b;">{code}</p>
      <p style="color: #777; font-size: 13px;">Bu kod 15 dəqiqə ərzində etibarlıdır. Əgər bu sorğunu siz göndərməmisinizsə, bu mesajı görməzdən gələ bilərsiniz.</p>
    </div>
    """

    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.sendmail(from_email, to_email, message.as_string())

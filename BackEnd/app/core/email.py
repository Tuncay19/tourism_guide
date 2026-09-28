import httpx

from app.core.config import settings

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def send_verification_email(to_email: str, code: str) -> bool:
    """
    Təsdiqləmə kodunu Brevo HTTP API ilə göndərir (SMTP yox — Render pulsuz
    planında SMTP portları bloklanıb). Uğurludursa True qaytarır.
    API açarı təyin olunmayıbsa, kodu sadəcə loglara yazır (inkişaf üçün).
    """
    if not settings.brevo_api_key or not settings.mail_sender_email:
        print(f"[DEV] {to_email} üçün təsdiqləmə kodu: {code}")
        return False

    text_body = f"Salam!\n\nEmail təsdiqləmə kodunuz: {code}\n\nBu kod 15 dəqiqə ərzində etibarlıdır."
    html_body = f"""
    <div style="font-family: Arial, sans-serif; padding: 24px; max-width: 480px; margin: 0 auto;">
      <h2 style="color: #2e7d32;">Email təsdiqləmə</h2>
      <p>Qeydiyyatınızı tamamlamaq üçün aşağıdakı kodu tətbiqdə daxil edin:</p>
      <p style="font-size: 32px; font-weight: bold; letter-spacing: 6px; color: #1b1b1b;">{code}</p>
      <p style="color: #777; font-size: 13px;">Bu kod 15 dəqiqə ərzində etibarlıdır. Əgər bu sorğunu siz göndərməmisinizsə, bu mesajı görməzdən gələ bilərsiniz.</p>
    </div>
    """

    payload = {
        "sender": {"name": settings.mail_sender_name, "email": settings.mail_sender_email},
        "to": [{"email": to_email}],
        "subject": "AzTurizm Guide — Email təsdiqləmə kodu",
        "htmlContent": html_body,
        "textContent": text_body,
    }
    headers = {"api-key": settings.brevo_api_key, "accept": "application/json"}

    try:
        response = httpx.post(BREVO_URL, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[EMAIL ERROR] {to_email}: {exc}")
        return False

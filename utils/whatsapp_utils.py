# utils/whatsapp_utils.py
from twilio.rest import Client

def send_whatsapp(to_number, body, account_sid, auth_token, from_number="whatsapp:+14155238886"):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=from_number,
        to=f"whatsapp:{to_number}"
    )
    return message.sid
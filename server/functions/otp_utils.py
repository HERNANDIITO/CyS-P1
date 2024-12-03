import pyotp

# Genera un secreto para el OTP
def generate_secret_key() -> str:
    return pyotp.random_base32()

# Verifica que un codigo temporal coincida con el secreto
def verify_otp(secret_key: str, otp):
    totp = pyotp.TOTP(secret_key)
    return totp.verify(otp)

# Genera una URL que se usa para generar el codigo QR
def generate_url(secret_key: str, user_email: str) -> str:
    return pyotp.totp.TOTP(secret_key).provisioning_uri(name=user_email, issuer_name='Asegurados')

import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings


if not firebase_admin._apps:
    cred = credentials.Certificate(
        settings.FIREBASE_SERVICE_ACCOUNT
    )

    firebase_admin.initialize_app(cred)


def verify_firebase_token(id_token):
    """
    Verify Firebase ID token and return decoded Firebase user data.
    """

    try:
        decoded_token = auth.verify_id_token(id_token)

        return decoded_token

    except Exception:
        return None